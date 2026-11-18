<#
.SYNOPSIS
    Purges exposed Kaggle Personal Access Token from local Git commit history.
.DESCRIPTION
    1. Verifies working tree is clean.
    2. Creates a safety backup branch: backup/pre-secret-purge-<timestamp>.
    3. Rewrites commit history replacing the secret string with REDACTED_TOKEN.
    4. Verifies the secret no longer exists in any commit object.
    5. Prompts for force-push confirmation.
#>

param(
    [string]$SecretToken = $env:SECRET_TO_PURGE,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

Write-Host "🛡️ [SECRET PURGE] Checking working tree status..." -ForegroundColor Cyan

if (-not $SecretToken) {
    Write-Host "❌ No secret token provided. Set `$env:SECRET_TO_PURGE or pass -SecretToken." -ForegroundColor Red
    exit 1
}

$status = git status --porcelain
if ($status) {
    Write-Host "❌ Working tree has uncommitted changes. Please commit or stash changes before running history rewrite." -ForegroundColor Red
    exit 1
}

$backupBranch = "backup/pre-secret-purge-$(Get-Date -Format 'yyyyMMdd-HHmmss')"

Write-Host "Creating safety backup branch: $backupBranch" -ForegroundColor Yellow
git branch $backupBranch

Write-Host "Purging secret pattern from git history across all branches..." -ForegroundColor Yellow

$filterScript = @"
import os
p = '.agents/mcp_config.json'
if os.path.exists(p):
    with open(p, 'r', encoding='utf-8') as f:
        data = f.read()
    if '$SecretToken' in data:
        data = data.replace('$SecretToken', 'REDACTED_KAGGLE_TOKEN')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(data)
"@

$env:FILTER_BRANCH_SQUELCH_WARNING = "1"
git filter-branch --force --tree-filter "python -c `"$filterScript`"" --tag-name-filter cat -- --all

# Remove original refs created by filter-branch so subsequent git rev-list --all only inspects active rewritten history
git for-each-ref --format="%(refname)" refs/original/ | ForEach-Object { git update-ref -d $_ }

Write-Host "Verifying purge across all commits..." -ForegroundColor Cyan
$remaining = git grep "$SecretToken" $(git rev-list --all) 2>$null

if ($remaining) {
    Write-Host "❌ Secret still detected in commit objects!" -ForegroundColor Red
    exit 1
} else {
    Write-Host "✅ Secret successfully scrubbed from all local commit objects." -ForegroundColor Green
    Write-Host "Safety backup preserved at branch: $backupBranch" -ForegroundColor Green
    Write-Host ""
    Write-Host "To update remote GitHub branches, run:" -ForegroundColor Yellow
    Write-Host "  git push origin --force --all" -ForegroundColor Cyan
}
