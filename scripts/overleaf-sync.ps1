<#
.SYNOPSIS
    Overleaf Live Synchronization Wrapper (overleaf-sync.ps1)
    Provides fast, sub-second bidirectional sync between local LaTeX documents and Overleaf.
.DESCRIPTION
    Uses Socket.IO OT updates via scripts/overleaf-sync.js.
.EXAMPLE
    pwsh -File .\scripts\overleaf-sync.ps1 -Push
    pwsh -File .\scripts\overleaf-sync.ps1 -Pull
    pwsh -File .\scripts\overleaf-sync.ps1 -Status
    pwsh -File .\scripts\overleaf-sync.ps1 -Status -Project "6af97ae4e99d9136ba9ad729"
#>

param(
    [switch]$Push,
    [switch]$Pull,
    [switch]$Status,
    [string]$Project = "6af97ae4e99d9136ba9ad729",
    [string]$File = "",
    [string]$Message = "",
    [switch]$NoCommit
)

$scriptPath = Join-Path $PSScriptRoot "overleaf-sync.js"
$action = "--status"
if ($Push) { $action = "--push" }
if ($Pull) { $action = "--pull" }

$nodeArgs = @($scriptPath, $action, "--project", $Project)
if ($File) { $nodeArgs += @("--file", $File) }
if ($NoCommit) { $nodeArgs += "--no-commit" }

node @nodeArgs
exit $LASTEXITCODE
