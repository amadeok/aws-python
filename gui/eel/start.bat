@echo off
Start "PROCESS1" node %AppData%\npm\node_modules\serve\build\main.js -s build 
react-eel-app.exe
taskkill /T /FI "WindowTitle eq PROCESS1"
