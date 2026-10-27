param([string]$Message = "v1.7.3场景事务与首帧稳定性优化")
$ErrorActionPreference = "Stop"
& "$PSScriptRoot\..\..\release-current.ps1" -Message $Message
