#!/usr/bin/env node

import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { dirname, join, resolve } from 'node:path';

const argumentIndex = process.argv.indexOf('--repo');
const requestedRepo = argumentIndex >= 0 ? process.argv[argumentIndex + 1] : undefined;
const repo = resolve(requestedRepo ?? process.env.NEXA_DESIGN_LAB_PATH ?? '/Users/diegosandoval284/Developer/nexa-suite/design-lab');
const asJson = process.argv.includes('--json');

const failures = [];

function source(relativePath) {
  const absolutePath = join(repo, relativePath);
  if (!existsSync(absolutePath)) {
    failures.push(`missing source: ${relativePath}`);
    return '';
  }
  return readFileSync(absolutePath, 'utf8');
}

function matches(text, pattern) {
  return [...text.matchAll(pattern)].map((match) => match[1]);
}

function unique(values) {
  return [...new Set(values)];
}

function filesUnder(directory) {
  if (!existsSync(directory)) return [];
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const path = join(directory, entry.name);
    return entry.isDirectory() ? filesUnder(path) : [path];
  });
}

function gitHead() {
  try {
    return execFileSync('git', ['-C', repo, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim();
  } catch {
    return 'unknown';
  }
}

const registry = source('src/app/documentation/navigation/documentation-registry.ts');
const routes = source('src/app/app.routes.ts');
const publicApi = source('projects/nexa-ui/src/public-api.ts');
const manifestText = source('tooling/visual-regression/manifest.json');
const contentDirectory = join(repo, 'src/app/documentation/content');
const libraryDirectory = join(repo, 'projects/nexa-ui/src/lib');

const pageIds = unique(matches(registry, /\bid:\s*'([^']+)'/g));
const pagePaths = unique(matches(registry, /\bpath:\s*'([^']+)'/g));
const contentFiles = filesUnder(contentDirectory).filter((path) => path.endsWith('-content.ts'));
const contentIds = unique(contentFiles.flatMap((path) => matches(readFileSync(path, 'utf8'), /\bid:\s*'([^']+)'/g)));
const missingContent = pageIds.filter((id) => !contentIds.includes(id));
const extraContent = contentIds.filter((id) => !pageIds.includes(id));

let manifest = { canonicalRoutes: [], requiredViewports: [], layoutViewports: [] };
try {
  manifest = JSON.parse(manifestText);
} catch {
  failures.push('invalid visual-regression manifest JSON');
}
const manifestPaths = (manifest.canonicalRoutes ?? []).map((route) => route.path);
const missingManifestRoutes = manifestPaths.filter((path) => !pagePaths.includes(path));

const exportedCandidates = matches(publicApi, /^export \{ (Nexa\w+) \}/gm);
const libraryFiles = filesUnder(libraryDirectory);
const candidateDetails = exportedCandidates.map((name) => {
  const implementation = libraryFiles.find((path) => readFileSync(path, 'utf8').includes(`export class ${name}`));
  if (!implementation) {
    failures.push(`missing implementation for public export: ${name}`);
    return { name, implementation: null, files: [], inputs: [], unions: [] };
  }
  const implementationText = readFileSync(implementation, 'utf8');
  const baseName = implementation.slice(0, -3);
  const related = libraryFiles.filter((path) => path.startsWith(`${baseName}.`));
  const required = ['.ts', '.html', '.spec.ts'];
  const missingFiles = required.filter((extension) => !related.some((path) => path === `${baseName}${extension}`));
  for (const missing of missingFiles) failures.push(`${name} missing colocated file: ${missing}`);
  const inputs = unique(matches(implementationText, /readonly\s+(\w+)\s*=\s*input(?:\.required)?/g));
  const models = unique(matches(implementationText, /readonly\s+(\w+)\s*=\s*model(?:\.required)?/g));
  const outputs = unique(matches(implementationText, /readonly\s+(\w+)\s*=\s*output/g));
  const unions = [...implementationText.matchAll(/export type\s+(\w+)\s*=\s*([^;]+);/g)]
    .map((match) => ({ name: match[1], definition: match[2].trim() }));
  return {
    name,
    selector: implementationText.match(/selector:\s*'([^']+)'/)?.[1] ?? null,
    implementation: implementation.replace(`${repo}/`, ''),
    files: related.map((path) => path.replace(`${repo}/`, '')),
    missingFiles,
    inputs,
    models,
    outputs,
    unions,
  };
});

if (missingContent.length) failures.push(`documentation content missing: ${missingContent.join(', ')}`);
if (extraContent.length) failures.push(`documentation content not registered: ${extraContent.join(', ')}`);
if (missingManifestRoutes.length) failures.push(`canonical routes missing from registry: ${missingManifestRoutes.join(', ')}`);

const report = {
  repo,
  sourceSha: gitHead(),
  documentation: {
    registeredPages: pageIds.length,
    contentPages: contentIds.length,
    missingContent,
    extraContent,
  },
  visualEvidence: {
    canonicalRoutes: manifestPaths.length,
    missingCanonicalRoutes: missingManifestRoutes,
    requiredViewports: [...(manifest.requiredViewports ?? []), ...(manifest.layoutViewports ?? [])],
  },
  publicApi: {
    exports: exportedCandidates.length,
    candidates: candidateDetails,
  },
  routeSourcePresent: routes.length > 0,
  failures,
};

if (asJson) {
  console.log(JSON.stringify(report, null, 2));
} else {
  console.log(`Nexa Design Lab audit: ${repo}`);
  console.log(`Source SHA: ${report.sourceSha}`);
  console.log(`Documentation: ${report.documentation.registeredPages} registered / ${report.documentation.contentPages} content`);
  console.log(`Canonical evidence routes: ${report.visualEvidence.canonicalRoutes}`);
  console.log(`Public reusable candidates: ${report.publicApi.exports}`);
  for (const candidate of candidateDetails) {
    console.log(`  ${candidate.name} (${candidate.selector ?? 'no selector'}): inputs=${candidate.inputs.join(', ') || 'none'} models=${candidate.models.join(', ') || 'none'} outputs=${candidate.outputs.join(', ') || 'none'}`);
  }
}

if (failures.length) {
  console.error('\nFailures:');
  for (const failure of failures) console.error(`- ${failure}`);
  process.exitCode = 1;
} else {
  if (!asJson) console.log('Coverage audit passed.');
}
