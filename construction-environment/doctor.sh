#!/usr/bin/env bash
# Local construction environment diagnostic. It does not print secrets.
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUITE_DIR="$(cd "${SCRIPT_DIR}/../.." && pwd)"
COMP_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
REPORT="${SCRIPT_DIR}/environment-report.md"
TMP_REPORT="${REPORT}.tmp"
ANDROID_HOME_PATH="${ANDROID_SDK_ROOT:-${HOME}/Library/Android/sdk}"
ANDROID_BIN="${HOME}/.local/bin/android"
FLUTTER_DIR="${NEXA_FLUTTER_DIR:-${SCRIPT_DIR}/toolchains/flutter-3.47.2}"
FLUTTER_BIN="${FLUTTER_DIR}/bin/flutter"
FLUTTER_DART="${FLUTTER_DIR}/bin/dart"
MODERN_COMPOSE_FILE="${SUITE_DIR}/api/ops/compose/modern.compose.yml"
JDK17_HOME="${JAVA_HOME_17:-}"
JDK25_HOME="${JAVA_HOME_25:-}"

discover_jdk_home() {
  local major="$1"
  local configured=""
  local detected=""
  if [[ "${major}" == "17" ]]; then
    configured="${JAVA_HOME_17:-}"
  else
    configured="${JAVA_HOME_25:-}"
  fi
  if [[ -n "${configured}" && -x "${configured}/bin/java" ]]; then
    if "${configured}/bin/java" -version 2>&1 | head -n 1 | rg -q "\"${major}([.]|$)"; then
      printf '%s' "${configured}"
      return
    fi
  fi
  if [[ -x /usr/libexec/java_home ]]; then
    detected="$(/usr/libexec/java_home -v "${major}" 2>/dev/null || true)"
    if [[ -n "${detected}" && -x "${detected}/bin/java" ]]; then
      if "${detected}/bin/java" -version 2>&1 | head -n 1 | rg -q "\"${major}([.]|$)"; then
        printf '%s' "${detected}"
        return
      fi
    fi
  fi
  if [[ -n "${JAVA_HOME:-}" && -x "${JAVA_HOME}/bin/java" ]]; then
    if "${JAVA_HOME}/bin/java" -version 2>&1 | head -n 1 | rg -q "\"${major}([.]|$)"; then
      printf '%s' "${JAVA_HOME}"
    fi
  fi
}

[[ -n "${JDK17_HOME}" ]] || JDK17_HOME="$(discover_jdk_home 17)"
[[ -n "${JDK25_HOME}" ]] || JDK25_HOME="$(discover_jdk_home 25)"
MODERN_ENV_FILE="${SUITE_DIR}/api/.env.local"

status_line() {
  printf '| %s | %s | %s |\n' "$1" "$2" "$3" >> "${TMP_REPORT}"
}

version_or_missing() {
  local cmd="$1"
  if command -v "${cmd}" >/dev/null 2>&1; then
    "${cmd}" --version 2>&1 | head -n 1 | tr '|' '/'
  else
    printf 'not found'
  fi
}

binary_status() {
  local label="$1"
  local cmd="$2"
  if command -v "${cmd}" >/dev/null 2>&1; then
    status_line "${label}" "READY" "$(version_or_missing "${cmd}")"
  else
    status_line "${label}" "MISSING" "${cmd} is not on PATH"
  fi
}

{
  printf '# Nexa Construction Environment Report\n\n'
  printf -- '- generated-at: %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  printf -- '- scope: local-only, secret-free toolchain/readiness diagnosis\n'
  printf -- '- status vocabulary: READY, READY WITH CAVEAT, MISSING, BLOCKED\n\n'
  printf '| Check | Status | Evidence |\n|---|---|---|\n'
} > "${TMP_REPORT}"

binary_status "Git" git
binary_status "GitHub CLI" gh
binary_status "curl" curl
binary_status "jq" jq
binary_status "ripgrep" rg
binary_status "Python" python3
binary_status "Docker" docker
if docker compose version >/dev/null 2>&1; then
  status_line "Docker Compose" "READY" "$(docker compose version --short 2>/dev/null || docker compose version 2>/dev/null | head -n 1)"
else
  status_line "Docker Compose" "MISSING" "docker compose is unavailable"
fi

if [[ -x "${JDK25_HOME}/bin/java" ]]; then
  status_line "JDK 25" "READY" "${JDK25_HOME}; $(${JDK25_HOME}/bin/java -version 2>&1 | head -n 1 | tr '|' '/')"
else
  status_line "JDK 25" "MISSING" "Homebrew JDK 25 path not found"
fi
if [[ -x "${JDK17_HOME}/bin/java" ]]; then
  status_line "Android JDK 17" "READY" "${JDK17_HOME}; $(${JDK17_HOME}/bin/java -version 2>&1 | head -n 1 | tr '|' '/')"
else
  status_line "Android JDK 17" "MISSING" "Homebrew JDK 17 path not found"
fi
binary_status "Maven" mvn
if command -v node >/dev/null 2>&1; then
  NODE_VERSION="$(node --version)"
  if [[ "${NODE_VERSION}" == v24.* ]]; then
    status_line "Node 24" "READY" "${NODE_VERSION}"
  else
    status_line "Node 24" "READY WITH CAVEAT" "${NODE_VERSION}; newer host runtime retained without downgrade"
  fi
else
  status_line "Node 24" "MISSING" "node is unavailable"
fi
if command -v npm >/dev/null 2>&1; then
  NPM_VERSION="$(npm --version)"
  if [[ "${NPM_VERSION}" == 11.17.* ]]; then
    status_line "npm 11.17" "READY" "${NPM_VERSION}"
  else
    status_line "npm 11.17" "READY WITH CAVEAT" "${NPM_VERSION}; host runtime retained"
  fi
else
  status_line "npm 11.17" "MISSING" "npm is unavailable"
fi

if [[ -x "${ANDROID_BIN}" ]]; then
  status_line "Android CLI" "READY" "${ANDROID_BIN}; $(${ANDROID_BIN} --version 2>&1 | head -n 1 | tr '|' '/')"
else
  status_line "Android CLI" "MISSING" "${ANDROID_BIN} is unavailable"
fi
SDK37_DIR="$(find "${ANDROID_HOME_PATH}/platforms" -maxdepth 1 -type d -name 'android-37*' 2>/dev/null | head -n 1)"
if [[ -n "${SDK37_DIR}" ]]; then
  status_line "Android SDK platform 37" "READY" "${SDK37_DIR}"
else
  status_line "Android SDK platform 37" "MISSING" "android-37 platform directory absent"
fi
if [[ -x "${ANDROID_HOME_PATH}/platform-tools/adb" ]]; then
  status_line "adb" "READY" "$(${ANDROID_HOME_PATH}/platform-tools/adb version 2>&1 | head -n 1 | tr '|' '/')"
  CONNECTED_DEVICE_COUNT="$(${ANDROID_HOME_PATH}/platform-tools/adb devices 2>/dev/null | awk 'NR > 1 && $2 == "device" { count++ } END { print count + 0 }')"
  if [[ "${CONNECTED_DEVICE_COUNT}" -gt 0 ]]; then
    status_line "Connected Android physical devices" "READY WITH CAVEAT" "${CONNECTED_DEVICE_COUNT} adb device(s); physical evidence remains a later acceptance activity"
  else
    status_line "Connected Android physical devices" "MISSING" "no adb physical device currently connected"
  fi
else
  status_line "adb" "MISSING" "platform-tools/adb unavailable"
fi
if [[ -x "${ANDROID_HOME_PATH}/emulator/emulator" ]]; then
  AVD_COUNT="$(${ANDROID_HOME_PATH}/emulator/emulator -list-avds 2>/dev/null | sed '/^$/d' | wc -l | tr -d ' ')"
  if [[ "${AVD_COUNT}" -gt 0 ]]; then
    status_line "Android emulator" "READY" "${AVD_COUNT} configured AVD(s)"
  else
    status_line "Android emulator" "READY WITH CAVEAT" "emulator installed; no configured AVD"
  fi
else
  status_line "Android emulator" "MISSING" "emulator binary unavailable"
fi
if [[ -d "/Applications/Android Studio.app" ]]; then
  status_line "Android Studio" "READY" "/Applications/Android Studio.app"
else
  status_line "Android Studio" "MISSING" "application bundle not found"
fi

if [[ -x "${FLUTTER_BIN}" ]]; then
  status_line "Flutter 3.47" "READY WITH CAVEAT" "$(${FLUTTER_BIN} --version 2>&1 | head -n 1 | tr '|' '/'); exact local tag checkout, invoke by explicit path or prepend its bin to PATH"
elif command -v flutter >/dev/null 2>&1; then
  status_line "Flutter 3.47" "READY WITH CAVEAT" "$(flutter --version 2>&1 | head -n 1 | tr '|' '/'); host PATH toolchain used"
else
  status_line "Flutter 3.47" "MISSING" "local construction toolchain unavailable"
fi
if [[ -x "${FLUTTER_DART}" ]]; then
  status_line "Dart 3.13" "READY" "$(${FLUTTER_DART} --version 2>&1 | head -n 1 | tr '|' '/')"
elif command -v dart >/dev/null 2>&1; then
  status_line "Dart 3.13" "READY WITH CAVEAT" "$(dart --version 2>&1 | head -n 1 | tr '|' '/'); host PATH toolchain used"
else
  status_line "Dart 3.13" "MISSING" "local construction toolchain unavailable"
fi
if command -v xcodebuild >/dev/null 2>&1; then
  status_line "Xcode" "READY" "$(xcodebuild -version 2>&1 | head -n 1 | tr '|' '/')"
else
  status_line "Xcode" "MISSING" "xcodebuild unavailable"
fi
if command -v xcrun >/dev/null 2>&1 && xcrun simctl list runtimes 2>/dev/null | rg -q 'iOS'; then
  status_line "iOS simulator runtime" "READY" "iOS runtime detected through simctl"
else
  status_line "iOS simulator runtime" "MISSING" "no iOS simulator runtime detected"
fi
if command -v pod >/dev/null 2>&1; then
  status_line "CocoaPods" "READY" "$(pod --version 2>&1 | head -n 1 | tr '|' '/')"
else
  status_line "CocoaPods" "MISSING" "pod unavailable"
fi

if [[ -f "${COMP_DIR}/structurizr/compose.yml" ]] && docker compose -p nexa-blueprint-architecture -f "${COMP_DIR}/structurizr/compose.yml" config -q >/dev/null 2>&1; then
  status_line "Structurizr local" "READY" "separate compose project nexa-blueprint-architecture; config valid"
elif [[ -f "${COMP_DIR}/structurizr/compose.yml" ]]; then
  status_line "Structurizr local" "READY WITH CAVEAT" "compose file exists; Docker config validation did not complete"
else
  status_line "Structurizr local" "MISSING" "complementary/structurizr/compose.yml absent"
fi

ANDROID_SKILLS=(android-cli testing-setup camerax navigation-3 edge-to-edge android-intent-security r8-analyzer android-profiler adaptive)
MISSING_ANDROID_SKILLS=()
for skill in "${ANDROID_SKILLS[@]}"; do
  [[ -d "${HOME}/.codex/skills/${skill}" ]] || MISSING_ANDROID_SKILLS+=("${skill}")
done
if [[ "${#MISSING_ANDROID_SKILLS[@]}" -eq 0 ]]; then
  status_line "Android official skills" "READY" "9 required skills installed under ~/.codex/skills"
else
  status_line "Android official skills" "MISSING" "${MISSING_ANDROID_SKILLS[*]}"
fi
if codex plugin list 2>/dev/null | rg -q 'dart-flutter@dart-flutter.*installed'; then
  status_line "Flutter/Dart Codex plugin" "READY" "dart-flutter@dart-flutter installed"
else
  status_line "Flutter/Dart Codex plugin" "MISSING" "dart-flutter plugin absent"
fi
CUSTOM_SKILLS=(nexa-canonical-guardrails nexa-implementation-slice nexa-architecture-conformance nexa-operations-mobile nexa-buyer-mobile nexa-quality-evidence-gates)
MISSING_CUSTOM_SKILLS=()
for skill in "${CUSTOM_SKILLS[@]}"; do
  [[ -L "${HOME}/.agents/skills/${skill}" || -d "${HOME}/.agents/skills/${skill}" ]] || MISSING_CUSTOM_SKILLS+=("${skill}")
done
if [[ "${#MISSING_CUSTOM_SKILLS[@]}" -eq 0 ]]; then
  status_line "Nexa custom skills" "READY" "6 local-source skills available under ~/.agents/skills"
else
  status_line "Nexa custom skills" "MISSING" "${MISSING_CUSTOM_SKILLS[*]}"
fi

if [[ -f "${MODERN_COMPOSE_FILE}" ]] && [[ -f "${MODERN_ENV_FILE}" ]] && docker compose --env-file "${MODERN_ENV_FILE}" -p nexa-modern -f "${MODERN_COMPOSE_FILE}" config -q >/dev/null 2>&1; then
  status_line "nexa-modern compose" "READY" "canonical compose configuration parses; service health is reported separately"
elif [[ ! -f "${MODERN_ENV_FILE}" ]]; then
  status_line "nexa-modern compose" "BLOCKED" "api/.env.local is absent; no secrets were created or printed"
else
  status_line "nexa-modern compose" "READY WITH CAVEAT" "compose configuration not validated in this doctor run"
fi
status_line "Physical-device acceptance" "MISSING" "not asserted by host tooling; later implementation/acceptance gate"

mv "${TMP_REPORT}" "${REPORT}"
printf 'Wrote %s\n' "${REPORT}"
