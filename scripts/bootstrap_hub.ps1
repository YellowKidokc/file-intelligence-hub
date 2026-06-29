param(
    [string]$RepoRoot = "D:\DONT TOUCH BOOT UP\file-intelligence-hub"
)

$ErrorActionPreference = "Stop"
Set-Location -LiteralPath $RepoRoot

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

$python = Join-Path $RepoRoot ".venv\Scripts\python.exe"
& $python -m pip install --upgrade pip
& $python -m pip install -r (Join-Path $RepoRoot "requirements.txt")

Write-Host ""
Write-Host "Bootstrap complete." -ForegroundColor Green
Write-Host "Python: $python"
Write-Host "Next: .\.venv\Scripts\python.exe .\scripts\compare_stack.py"
