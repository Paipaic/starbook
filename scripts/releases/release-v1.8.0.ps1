param(
    [string]$Message = "v1.8.0架构扩展与交互体验升级"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.8.0" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.8.0" -Message $Message