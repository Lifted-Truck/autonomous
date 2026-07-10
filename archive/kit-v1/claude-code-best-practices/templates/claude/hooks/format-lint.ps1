# PostToolUse hook (PowerShell) — deterministic format/lint of the file Claude just
# edited. Reads the tool-call JSON from stdin, extracts the file path, runs the
# matching formatter if installed. Always exits 0 (never blocks the edit).
$ErrorActionPreference = 'SilentlyContinue'

$payload = [Console]::In.ReadToEnd()
try { $file = ($payload | ConvertFrom-Json).tool_input.file_path } catch { $file = $null }
if (-not $file -or -not (Test-Path $file)) { exit 0 }

function Has($c) { [bool](Get-Command $c -ErrorAction SilentlyContinue) }

switch -Regex ($file) {
  '\.(ts|tsx|js|jsx|json|css|md)$' { if (Has npx)          { npx --no-install prettier --write $file 2>$null } }
  '\.py$'                          { if (Has ruff)         { ruff format $file 2>$null; ruff check --fix $file 2>$null } }
  '\.go$'                          { if (Has gofmt)        { gofmt -w $file 2>$null } }
  '\.rs$'                          { if (Has rustfmt)      { rustfmt $file 2>$null } }
  '\.(c|cc|cpp|h|hpp)$'            { if (Has clang-format) { clang-format -i $file 2>$null } }
  '\.cs$'                          { if (Has dotnet)       { dotnet format --include $file 2>$null } }
}

exit 0
