#!/bin/sh

NEXA_TOOLS_ROOT=${NEXA_TOOLS_ROOT:-$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)}
NEXA_CONTRIBUTORS_FILE=${NEXA_CONTRIBUTORS_FILE:-"$NEXA_TOOLS_ROOT/signing/contributors.conf"}

nexa_expand_home() {
  case "$1" in
    '$HOME/'*) printf '%s/%s\n' "$HOME" "${1#\$HOME/}";;
    '~/'*) printf '%s/%s\n' "$HOME" "${1#\~/}";;
    *) printf '%s\n' "$1";;
  esac
}

nexa_record() {
  awk -F '|' -v wanted="$1" 'NF == 5 && $1 == wanted { print; found++ } END { if (found != 1) exit 1 }' "$NEXA_CONTRIBUTORS_FILE"
}

nexa_records() {
  awk -F '|' 'NF == 5 && $1 !~ /^[[:space:]]*#/ { print }' "$NEXA_CONTRIBUTORS_FILE"
}

nexa_allowed_signers_file() {
  printf '%s\n' "$HOME/.ssh/nexa_allowed_signers"
}

nexa_agent_has_key() {
  pub_file=$1
  key_type=$(awk 'NF >= 2 { print $1; exit }' "$pub_file")
  key_blob=$(awk 'NF >= 2 { print $2; exit }' "$pub_file")
  [ -n "$key_type" ] && [ -n "$key_blob" ] || return 1
  ssh-add -L 2>/dev/null | awk -v wanted_type="$key_type" -v wanted_blob="$key_blob" '$1 == wanted_type && $2 == wanted_blob { found = 1 } END { exit(found ? 0 : 1) }'
}

nexa_agent_is_healthy() {
  ssh-add -l >/dev/null 2>&1
  agent_status=$?
  [ "$agent_status" -eq 0 ] || [ "$agent_status" -eq 1 ]
}
