@echo off
cd .\env_eel\Scripts
call activate
pip3.10 install -r ..\..\requirements.txt
cd ..\..
if exist build\react-eel-app rmdir /s /q build\react-eel-app
if exist dist rmdir /s /q dist
C:\Users\amade\AppData\Local\Programs\Python\Python310\python -m eel index.py build --onefile --name react-eel-app -w
x