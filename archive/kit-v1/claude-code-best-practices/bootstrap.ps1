<#
.SYNOPSIS
  Drop the claude-optimization harness into a target repo.

.DESCRIPTION
  Detects project type, fills in test/lint/format commands and the hook invocations
  for your chosen shell, and copies the templates in. Non-destructive: existing files
  are skipped unless -Force. Use -DryRun to preview.

.EXAMPLE
  .\bootstrap.ps1 -TargetPath C:\code\my-repo
.EXAMPLE
  .\bootstrap.ps1 -TargetPath C:\code\my-repo -Shell sh -DryRun
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)] [string] $TargetPath,
  [string] $ProjectName,
  [ValidateSet('pwsh', 'sh')] [string] $Shell = 'pwsh',
  [switch] $Force,
  [switch] $DryRun
)

$ErrorActionPreference = 'Stop'
$kit = $PSScriptRoot
$tpl = Join-Path $kit 'templates'

if (-not (Test-Path $TargetPath)) { throw "Target path does not exist: $TargetPath" }
$TargetPath = (Resolve-Path $TargetPath).Path
if (-not $ProjectName) { $ProjectName = Split-Path $TargetPath -Leaf }

# --- Detect project type & commands -----------------------------------------
function Test-File($p) { Test-Path (Join-Path $TargetPath $p) }
function Test-Glob($g) { (Get-ChildItem -Path $TargetPath -Filter $g -ErrorAction SilentlyContinue | Select-Object -First 1) }

$type = 'unknown'; $test = '<configure test cmd>'; $lint = '<configure lint cmd>'; $fmt = '<configure format cmd>'
if     (Test-File 'package.json')                              { $type='node';   $test='npm test';        $lint='npm run lint';      $fmt='npx prettier --write .' }
elseif ((Test-File 'pyproject.toml') -or (Test-File 'requirements.txt')) { $type='python'; $test='pytest'; $lint='ruff check .';     $fmt='ruff format .' }
elseif (Test-File 'Cargo.toml')                               { $type='rust';   $test='cargo test';      $lint='cargo clippy';      $fmt='cargo fmt' }
elseif (Test-File 'go.mod')                                   { $type='go';     $test='go test ./...';   $lint='go vet ./...';      $fmt='gofmt -w .' }
elseif ((Test-Glob '*.sln') -or (Test-Glob '*.csproj'))       { $type='dotnet'; $test='dotnet test';     $lint='dotnet build';      $fmt='dotnet format' }
elseif (Test-File 'CMakeLists.txt')                           { $type='cpp';    $test='ctest';           $lint='clang-tidy';        $fmt='clang-format -i' }

# --- Hook command strings for the chosen shell ------------------------------
if ($Shell -eq 'pwsh') {
  $h = { param($n) "pwsh -NoProfile -File .claude/hooks/$n.ps1" }
} else {
  $h = { param($n) "bash .claude/hooks/$n.sh" }
}
$subs = @{
  '{{PROJECT_NAME}}'       = $ProjectName
  '{{PROJECT_TYPE}}'       = $type
  '{{TEST_CMD}}'           = $test
  '{{LINT_CMD}}'           = $lint
  '{{FORMAT_CMD}}'         = $fmt
  '{{FORMAT_LINT_HOOK}}'   = (& $h 'format-lint')
  '{{SESSION_START_HOOK}}' = (& $h 'session-start-context')
  '{{STOP_HOOK}}'          = (& $h 'stop-capture-learnings')
}

Write-Host "claude-optimization bootstrap" -ForegroundColor Cyan
Write-Host "  target : $TargetPath"
Write-Host "  project: $ProjectName  (detected type: $type)"
Write-Host "  shell  : $Shell$(if($DryRun){'   [DRY RUN]'})"
Write-Host ""

# --- Copy engine -------------------------------------------------------------
function Deploy($srcRel, $dstRel, [bool]$substitute) {
  $src = Join-Path $tpl $srcRel
  $dst = Join-Path $TargetPath $dstRel
  if (-not (Test-Path $src)) { Write-Host "  ! missing template: $srcRel" -ForegroundColor Yellow; return }
  if ((Test-Path $dst) -and -not $Force) { Write-Host "  skip   $dstRel (exists)" -ForegroundColor DarkGray; return }
  $action = if (Test-Path $dst) { 'over' } else { 'write' }
  if ($DryRun) { Write-Host "  $action  $dstRel" -ForegroundColor DarkCyan; return }
  $dir = Split-Path $dst -Parent
  if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
  if ($substitute) {
    $c = Get-Content $src -Raw
    foreach ($k in $subs.Keys) { $c = $c.Replace($k, $subs[$k]) }
    Set-Content -Path $dst -Value $c -NoNewline -Encoding UTF8
  } else {
    Copy-Item $src $dst -Force
  }
  Write-Host "  $action  $dstRel" -ForegroundColor Green
}

# Root docs / config (substituted)
Deploy 'CLAUDE.root.md' 'CLAUDE.md'        $true
Deploy 'CODEMAP.md'     'CODEMAP.md'       $true
Deploy '.claudeignore'  '.claudeignore'    $false

# .claude/ config
Deploy 'claude/settings.json'                       '.claude/settings.json'                       $true
Deploy 'claude/.mcp.json'                           '.mcp.json'                                   $false
Deploy 'claude/agents/codebase-mapper.md'           '.claude/agents/codebase-mapper.md'           $false
Deploy 'claude/skills/example-domain/SKILL.md'      '.claude/skills/example-domain/SKILL.md'      $false
Deploy 'CLAUDE.subdir.md'                           '.claude/templates/CLAUDE.subdir.md'          $true

# Hooks — deploy the variant matching the chosen shell
$ext = if ($Shell -eq 'pwsh') { 'ps1' } else { 'sh' }
foreach ($n in 'format-lint','session-start-context','stop-capture-learnings') {
  Deploy "claude/hooks/$n.$ext" ".claude/hooks/$n.$ext" $false
}

Write-Host ""
Write-Host "Done. Next:" -ForegroundColor Cyan
Write-Host "  1. Edit $ProjectName/CLAUDE.md  — keep it to pointers + gotchas."
Write-Host "  2. Fill in CODEMAP.md with the real layout."
Write-Host "  3. Work through the kit's docs/CHECKLIST.md and assign an owner in docs/GOVERNANCE.md."
if ($type -eq 'unknown') { Write-Host "  !  Project type not detected — set test/lint/format commands in CLAUDE.md manually." -ForegroundColor Yellow }
