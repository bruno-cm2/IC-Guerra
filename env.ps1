$global:nw = "$PSScriptRoot\venv\Lib\site-packages\nodejs_wheel"
$env:Path = "$nw;$env:Path"
function global:npm { & "$nw\node.exe" "$nw\lib\node_modules\npm\bin\npm-cli.js" @args }
function global:npx { & "$nw\node.exe" "$nw\lib\node_modules\npm\bin\npx-cli.js" @args }