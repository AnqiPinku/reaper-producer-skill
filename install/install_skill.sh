#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
source_dir="$repo_root/skills/reaper-producer"
dest_root="${CODEX_HOME:-$HOME/.codex}/skills"
dest_dir="$dest_root/reaper-producer"

if [[ ! -d "$source_dir" ]]; then
  echo "Source skill not found: $source_dir" >&2
  exit 1
fi

mkdir -p "$dest_root"

if [[ -d "$dest_dir" ]]; then
  stamp="$(date +%Y%m%d-%H%M%S)"
  backup="$dest_dir.backup.$stamp"
  cp -R "$dest_dir" "$backup"
  echo "Backed up existing skill to $backup"
fi

rm -rf "$dest_dir"
cp -R "$source_dir" "$dest_dir"
echo "Installed reaper-producer skill to $dest_dir"
echo "Restart Codex or start a new thread before using the skill."

