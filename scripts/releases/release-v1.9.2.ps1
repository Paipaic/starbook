param(
    [string]$Message = "v1.9.2版本更新"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.9.2" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.9.2" -Message $Message