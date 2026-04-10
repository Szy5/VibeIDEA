param(
    [ValidateSet("crawl-official", "enrich", "export", "run-all", "stats")]
    [string]$Command = "run-all",
    [string[]]$Venues = @("AAAI", "ACL", "EMNLP"),
    [int[]]$Years = @(2023, 2024, 2025),
    [int]$EnrichLimit = 0,
    [string]$LogLevel = "INFO"
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

$argsList = @("-m", "backend.conference_crawler", "--log-level", $LogLevel, $Command)

if ($Command -in @("crawl-official", "enrich", "export", "run-all")) {
    $argsList += "--venues"
    $argsList += $Venues
    $argsList += "--years"
    $argsList += ($Years | ForEach-Object { "$_" })
}

if ($Command -eq "enrich" -and $EnrichLimit -gt 0) {
    $argsList += "--limit"
    $argsList += "$EnrichLimit"
}

if ($Command -eq "run-all" -and $EnrichLimit -gt 0) {
    $argsList += "--enrich-limit"
    $argsList += "$EnrichLimit"
}

Write-Host "Running: python $($argsList -join ' ')" -ForegroundColor Cyan
python @argsList
