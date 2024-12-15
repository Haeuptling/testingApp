REM scp -r "C:\Users\Tristan\OneDrive\Desktop\testingApp" raspberry@192.168.0.83:/home/raspberry/
@echo off
setlocal

set SRC_DIR=^"C:\Users\Tristan Lilienthal\Documents\testingApp"
set DEST_DIR=raspberry@10.155.20.174:/home/raspberry/testingApp

scp -r %SRC_DIR%\controls %DEST_DIR%
scp -r %SRC_DIR%\images %DEST_DIR%
scp -r %SRC_DIR%\models %DEST_DIR%
scp -r %SRC_DIR%\views %DEST_DIR%
scp -r %SRC_DIR%\main.py %DEST_DIR%
endlocal