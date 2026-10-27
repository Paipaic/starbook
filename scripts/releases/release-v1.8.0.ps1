param([string]$Message = "v1.8.0秘境之门转场、星辉层次与地球搜索")
$ErrorActionPreference = "Stop"
& "$PSScriptRoot\..\..\release-current.ps1" -Message $Message
