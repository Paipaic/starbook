param([string]$Message = "v1.8.1柔光分路转场、星夜魔法书、菜单精简与时光长卷")
$ErrorActionPreference = "Stop"
& "$PSScriptRoot\..\..\release-current.ps1" -Message $Message
