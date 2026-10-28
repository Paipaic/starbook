param([string]$Message = "v1.9.1照片分组、自动/手动放映与搜索面板去掉数据来源行")
$ErrorActionPreference = "Stop"
& "$PSScriptRoot\..\..\release-current.ps1" -Message $Message
