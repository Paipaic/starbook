param(
    [string]$Message = "v1.7.2性能、照片加载与响应式比例优化"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.7.2" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.7.2" -Message $Message