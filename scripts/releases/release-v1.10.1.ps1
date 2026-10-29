param(
    [string]$Message = "v1.10.1版本更新"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.10.1" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.10.1" -Message $Message