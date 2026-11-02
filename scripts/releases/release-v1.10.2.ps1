param(
    [string]$Message = "v1.10.2时光剪影进度条与尾声、返回原位、拖动稳定与安卓性能"
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
Set-Location $Root

Write-Host "Publishing Starbook v1.10.2" -ForegroundColor Cyan
& (Join-Path $Root "publish.ps1") -Version "1.10.2" -Message $Message
