param(
    [string]$Message = "v1.8.2移动端与性能优化"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.8.2" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.8.2" -Message $Message