param(
    [string]$Message = "v1.12.2城市真实位置 · 省份中文名 · 忘记密码"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.12.2" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.12.2" -Message $Message