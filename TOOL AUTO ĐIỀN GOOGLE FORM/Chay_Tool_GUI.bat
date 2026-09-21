@echo off
chcp 65001 >nul
title TOOL AUTO ĐIỀN GOOGLE FORM
cd /d "%~dp0"
python main_gui.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Co loi xay ra khi chay Tool. Vui long kiem tra Python da duoc cai dat chua.
    pause
)
