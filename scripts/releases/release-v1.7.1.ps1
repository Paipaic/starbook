param(
    [string]$Message = "v1.7.1 city-album功能优化更新"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.7.1" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.7.1" -Message $Message