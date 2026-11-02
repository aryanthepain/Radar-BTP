<#
.SYNOPSIS
  Invoke-Subagent - Asymmetric Worker Subagent Runner for Antigravity (2026)

.DESCRIPTION
  Delegates research, code generation, adversarial review, or log compression
  to fast/cheap worker submodels (Groq LPU, Mistral Codestral, Gemini, OpenRouter) to keep
  the primary Orchestrator context lean (<600 tokens).

.EXAMPLE
  pwsh -File .\scripts\Invoke-Subagent.ps1 -Task research -Query "Explain auth flow" -Files "src/auth.ts"
  pwsh -File .\scripts\Invoke-Subagent.ps1 -Task code -Prompt "Add UUID generator" -File "src/utils.ts"
  pwsh -File .\scripts\Invoke-Subagent.ps1 -Task review -Diff
  pwsh -File .\scripts\Invoke-Subagent.ps1 -ListModels -Sort intelligence
#>

[CmdletBinding()]
param(
  [Parameter(Mandatory=$false)]
  [ValidateSet('research', 'code', 'review', 'compress', 'ask')]
  [string]$Task = 'ask',

  [Parameter(Mandatory=$false)]
  [string]$Query,

  [Parameter(Mandatory=$false)]
  [string]$Prompt,

  [Parameter(Mandatory=$false)]
  [string]$Files,

  [Parameter(Mandatory=$false)]
  [string]$File,

  [Parameter(Mandatory=$false)]
  [switch]$Diff,

  [Parameter(Mandatory=$false)]
  [ValidateSet('fast', 'code', 'reasoning', 'cheap')]
  [string]$Tier = 'fast',

  [Parameter(Mandatory=$false)]
  [string]$Model,

  [Parameter(Mandatory=$false)]
  [int]$MaxTokens = 1024,

  [Parameter(Mandatory=$false)]
  [string]$Provider,

  [Parameter(Mandatory=$false)]
  [ValidateSet('auto', 'groq', 'direct')]
  [string]$Router = 'auto',

  [Parameter(Mandatory=$false)]
  [ValidateSet('intelligence', 'latest', 'code', 'reasoning', 'context')]
  [string]$Sort = 'intelligence',

  [Parameter(Mandatory=$false)]
  [switch]$ListModels,

  [Parameter(Mandatory=$false)]
  [switch]$RefreshModels,

  [Parameter(Mandatory=$false)]
  [switch]$Json,

  [Parameter(Mandatory=$false)]
  [switch]$Help
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$subagentJs = Join-Path $scriptDir "subagent.js"

if (-not (Test-Path $subagentJs)) {
  $subagentJs = Join-Path $env:USERPROFILE ".gemini\config\scripts\subagent.js"
}

if (-not (Test-Path $subagentJs)) {
  Write-Error "subagent.js not found in script directory or ~/.gemini/config/scripts/"
  exit 1
}

if ($Help) {
  & node $subagentJs --help
  exit 0
}

if ($ListModels) {
  & node $subagentJs --list-models --sort $Sort
  exit 0
}

if ($RefreshModels) {
  & node $subagentJs --refresh-models
  exit 0
}

$argList = @("--task", $Task)

if ($Query) { $argList += @("--query", $Query) }
if ($Prompt) { $argList += @("--prompt", $Prompt) }
if ($Files) { $argList += @("--files", $Files) }
if ($File) { $argList += @("--file", $File) }
if ($Diff) { $argList += @("--diff") }
if ($Tier) { $argList += @("--tier", $Tier) }
if ($Model) { $argList += @("--model", $Model) }
if ($MaxTokens) { $argList += @("--max-tokens", $MaxTokens) }
if ($Provider) { $argList += @("--provider", $Provider) }
if ($Router) { $argList += @("--router", $Router) }
if ($Sort) { $argList += @("--sort", $Sort) }
if ($Json) { $argList += @("--json") }

& node $subagentJs @argList
