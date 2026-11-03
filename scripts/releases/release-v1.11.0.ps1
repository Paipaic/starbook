param(
    [string]$Message = "v1.11.0国家星门面板（时空裂隙）"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.11.0" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.11.0" -Message $Message
