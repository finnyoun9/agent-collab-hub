$ErrorActionPreference = "Stop"

$appId = [Environment]::GetEnvironmentVariable("LARK_APP_ID", "User")
$appSecret = [Environment]::GetEnvironmentVariable("LARK_APP_SECRET", "User")

if (-not $appId -or -not $appSecret) {
    throw "Configure LARK_APP_ID and LARK_APP_SECRET in Windows user environment variables first."
}

$env:LARK_APP_ID = $appId
$env:LARK_APP_SECRET = $appSecret
$env:GITHUB_REPO = "finnyoun9/agent-collab-hub"
$env:COLLAB_LANG = "zh"
$env:GH_PATH = "C:\Program Files\GitHub CLI\gh.exe"

$node = "C:\Users\yyfxy\AppData\Local\hermes\node\node.exe"
if (-not (Test-Path -LiteralPath $node)) {
    $node = "node"
}

& $node "$PSScriptRoot\dist\index.js"
