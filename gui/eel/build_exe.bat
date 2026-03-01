@echo off
cd .\env_eel\Scripts
call activate
F:\all\GitHub\aws-python\gui\eel\env_eel\Scripts\pip3.10.exe install -r requirements.txt
cd ..\..
if exist build\react-eel-app rmdir /s /q build\react-eel-app
if exist dist rmdir /s /q dist
F:\all\GitHub\aws-python\gui\eel\env_eel\Scripts\python.exe -m eel index.py build --onefile --paths="F:\all\GitHub\aws-python" --name react-eel-app -w
