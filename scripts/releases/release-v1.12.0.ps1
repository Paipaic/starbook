param(
    [string]$Message = "v1.12.0数据安全：最近删除回收站与导出整本书"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.12.0" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.12.0" -Message $Message
