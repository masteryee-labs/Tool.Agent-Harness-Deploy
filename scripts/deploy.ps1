<#
.SYNOPSIS
  Tool.Agent-Harness-Deploy — manual deploy (Windows PowerShell).
.DESCRIPTION
  Detects installed AI tools, syncs the canonical harness into each, verifies.
  Equivalent to: python scripts/distill.py
  Use this when you want to deploy without an AI assistant driving it.
#>
param(
    [switch]$Global,
    [switch]$DryRun,
    [string]$Tools
)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

Write-Host "== Tool.Agent-Harness-Deploy — Manual Deploy (PowerShell) ==" -ForegroundColor Cyan

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: python not found on PATH. Install Python 3.9+." -ForegroundColor Red
    exit 1
}

$args = @("scripts/distill.py")
if ($Global) { $args += "--global" }
if ($DryRun) { $args += "--dry-run" }
if ($Tools) { $args += "--tools"; $args += $Tools }

python @args
exit $LASTEXITCODE
