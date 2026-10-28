param([string]$Message = "v1.8.2回到魔法书、星尘启封与手机性能修复")
$ErrorActionPreference = "Stop"
& "$PSScriptRoot\..\..\release-current.ps1" -Message $Message
