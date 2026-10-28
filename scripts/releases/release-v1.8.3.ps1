param(
    [string]$Message = "v1.8.3版本更新"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.8.3" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.8.3" -Message $Message