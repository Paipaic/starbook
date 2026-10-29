param(
    [string]$Message = "v1.10.0时光之环、时光剪影与背景音乐自动循环"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.10.0" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.10.0" -Message $Message
