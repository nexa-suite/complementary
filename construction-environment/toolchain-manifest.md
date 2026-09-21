# Toolchain Manifest

- recorded-at: 2026-09-20
- scope: local construction environment; no secrets or signing configuration

| Area | Required/accepted construction baseline | Detected local evidence | Status |
|---|---|---|---|
| API runtime | Java 25 | Homebrew OpenJDK 25.0.4 path retained | READY |
| Android build | JDK 17 | Homebrew OpenJDK 17.0.19 path retained | READY |
| Maven | 3.9.x | 3.9.16 | READY |
| Web | Node 24, npm 11.17.x | Node 26.5.0; npm 11.17.0 | READY WITH CAVEAT — newer Node retained |
| Android | API 37, platform-tools, emulator, Android CLI | SDK/platform 37, adb 37, emulator 37.1.11, CLI 1.0.16261425 | READY |
| Operations Mobile | Kotlin 2.4.20; Compose BOM 2026.09.00; AGP 9.4.x; Gradle 9.6.x | construction baseline recorded; no app scaffold created | TARGET ONLY |
| Buyer Mobile | Flutter 3.47.2; Dart 3.13.2 | local isolated `toolchains/flutter-3.47.2` at Flutter 3.47.2 / Dart 3.13.2 | READY WITH CAVEAT — use explicit local path or prepend its `bin` to PATH |
| Apple | Xcode, iOS runtime, SwiftPM, CocoaPods | Xcode 26.4.1; iOS simulator runtime; CocoaPods 1.17.0 | READY |
| Container tooling | Docker and Compose | Docker 29.7.2; Compose 5.4.0 | READY |
| C4 rendering | isolated Structurizr | `../structurizr/compose.yml`, project `nexa-blueprint-architecture` | READY WITH CAVEAT — runtime health is local Docker state |

The global host Flutter 3.44.7/Dart 3.12.2 was not replaced. The local 3.47.2 checkout is used by explicit path for Buyer construction. No physical-device evidence is claimed here.
