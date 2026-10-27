param(
    [string]$Message = "Starbook v1.7.0 release"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.7.0" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.7.0" -Message $Message