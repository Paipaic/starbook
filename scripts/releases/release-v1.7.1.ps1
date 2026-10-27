param(
    [string]$Message = "城市回忆目录页「星屿手稿 · 目录页」升级"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.7.1" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.7.1" -Message $Message
