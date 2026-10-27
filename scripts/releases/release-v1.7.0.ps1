param(
    [string]$Message = "光影放映：多图编排放映、三种放映风格、四季主题与编辑器升级"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.7.0" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.7.0" -Message $Message
