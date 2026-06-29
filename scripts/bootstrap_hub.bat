@echo off
cd /d "%~dp0\.."
powershell -ExecutionPolicy Bypass -File "%cd%\scripts\bootstrap_hub.ps1"
pause
