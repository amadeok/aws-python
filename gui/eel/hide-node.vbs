Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c node %AppData%\npm\node_modules\serve\build\main.js -s build"
oShell.Run strArgs, 0, false