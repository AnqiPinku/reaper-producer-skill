$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$source = Join-Path $repoRoot "skills\reaper-producer"
$destRoot = Join-Path $HOME ".codex\skills"
$dest = Join-Path $destRoot "reaper-producer"

if (-not (Test-Path -LiteralPath $source)) {
  throw "Source skill not found: $source"
}

if (-not (Test-Path -LiteralPath $destRoot)) {
  New-Item -ItemType Directory -Path $destRoot | Out-Null
}

if (Test-Path -LiteralPath $dest) {
  $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
  $backup = "$dest.backup.$stamp"
  Copy-Item -LiteralPath $dest -Destination $backup -Recurse -Force
  Write-Output "Backed up existing skill to $backup"
}

Copy-Item -LiteralPath $source -Destination $destRoot -Recurse -Force
Write-Output "Installed reaper-producer skill to $dest"
Write-Output "Restart Codex or start a new thread before using the skill."

