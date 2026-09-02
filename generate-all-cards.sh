#!/usr/bin/env bash

set -uo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
command_dir="$repo_root/card-commands"

shopt -s nullglob
commands=("$command_dir"/*.sh)

if ((${#commands[@]} == 0)); then
  printf 'No card commands found in %s\n' "$command_dir" >&2
  exit 1
fi

# Make commands that use either `python` or `.venv/bin/python` run through the
# project virtual environment when it is available.
if [[ -x "$repo_root/.venv/bin/python" ]]; then
  export PATH="$repo_root/.venv/bin:$PATH"
fi

cd "$repo_root" || exit 1

failures=()
index=0
for command_path in "${commands[@]}"; do
  ((index += 1))
  command_name="$(basename "$command_path")"
  printf '\n[%d/%d] Generating %s\n' \
    "$index" \
    "${#commands[@]}" \
    "${command_name%.sh}"

  if ! bash "$command_path"; then
    failures+=("$command_name")
  fi
done

printf '\nGenerated %d of %d cards.\n' \
  "$((${#commands[@]} - ${#failures[@]}))" \
  "${#commands[@]}"

if ((${#failures[@]} > 0)); then
  printf 'Failed commands:\n' >&2
  printf '  %s\n' "${failures[@]}" >&2
  exit 1
fi
