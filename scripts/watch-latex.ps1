<#
.SYNOPSIS
    Continuous LaTeX Auto-Builder and Watcher (watch-latex.ps1)
    Monitors .tex and .bib changes and recompiles via latexmk into build/.
.DESCRIPTION
    Uses latexmk -pvc -pdf with auxiliary folder caching.
.EXAMPLE
    pwsh -File .\scripts\watch-latex.ps1
    pwsh -File .\scripts\watch-latex.ps1 -Target "report.tex"
#>

param(
    [string]$Target = "report.tex"
)

if (-not (Test-Path $Target)) {
    if (Test-Path "templates/BTP_Report_Template_Overleaf/General_Report_Template.tex") {
        $Target = "templates/BTP_Report_Template_Overleaf/General_Report_Template.tex"
    } elseif (Test-Path "General_Report_Template.tex") {
        $Target = "General_Report_Template.tex"
    } else {
        Write-Error "Could not find target TeX file '$Target'."
        exit 1
    }
}

Write-Host "🔍 [LATEX WATCH] Starting continuous build on $Target (auxdir: build)..." -ForegroundColor Cyan

if (-not (Test-Path "build")) {
    New-Item -ItemType Directory -Path "build" | Out-Null
}

latexmk -pvc -pdf -interaction=nonstopmode -halt-on-error -auxdir=build $Target
exit $LASTEXITCODE
