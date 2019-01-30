@echo off
title EnterpRyze by gestalt8003
call env\Scripts\activate.bat
cd core
cls
echo Starting...
py -3.6 bot.py
pause