param([string]$Message = "v1.8.3开书机关启封特效")
$ErrorActionPreference = "Stop"
& "$PSScriptRoot\..\..\release-current.ps1" -Message $Message
