# WSL2 AMBER Bridge — Claude Code Agent Control
# 解决 Git Bash 路径映射失败的问题
# 用法: .\wsl_amber_bridge.ps1 -Script "run_prod.sh" [-Background]

param(
    [Parameter(Mandatory=$true)]$Script,
    [switch]$Background
)

$WSL_SCRIPT_PATH = "/home/klein/$Script"

# 1. 通过 UNC 路径拷贝脚本到 WSL
$source = "C:\Users\26404\Desktop\My Paper\2\04_验\$Script"
$target = "\\wsl.localhost\Ubuntu\home\klein\$Script"
Copy-Item $source $target -Force
Write-Host "[BRIDGE] Copied $Script to WSL"

# 2. 在 WSL 内执行
if ($Background) {
    wsl bash -c "nohup bash $WSL_SCRIPT_PATH > $WSL_SCRIPT_PATH.log 2>&1 &"
    Write-Host "[BRIDGE] Background started: $Script"
} else {
    wsl bash $WSL_SCRIPT_PATH
    Write-Host "[BRIDGE] Done: $Script"
}
