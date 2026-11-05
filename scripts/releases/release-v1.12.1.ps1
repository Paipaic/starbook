param(
    [string]$Message = "v1.12.1从备份导入：与导出格式对应的重新导入"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.12.1" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.12.1" -Message $Message
