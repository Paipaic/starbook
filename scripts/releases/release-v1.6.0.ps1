param(
    [string]$Message = "冥想盆放映厅：电影式回忆放映与放映按钮"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.6.0" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.6.0" -Message $Message
