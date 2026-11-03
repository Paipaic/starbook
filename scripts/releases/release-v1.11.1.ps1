param(
    [string]$Message = "v1.11.1复盘小优化：锁定依赖 · 抽屉下拉关闭 · 降耗 · 仓库整理"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.11.1" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.11.1" -Message $Message