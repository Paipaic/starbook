param([string]$Message = "v1.9.0行政区划搜索、影像管理台与星盘启封登录界面")
$ErrorActionPreference = "Stop"
& "$PSScriptRoot\..\..\release-current.ps1" -Message $Message
