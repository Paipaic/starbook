param(
    [string]$Message = "v1.10.1时光之环优化、日期精确到日、纪念日与魔法书星空背景"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.10.1" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.10.1" -Message $Message
