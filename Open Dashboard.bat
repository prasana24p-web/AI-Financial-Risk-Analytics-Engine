@echo off
setlocal
cd /d "%~dp0"

py -3.12 -c "import fastapi, httpx, streamlit, uvicorn" >nul 2>nul
if errorlevel 1 (
    echo Required Python packages are missing.
    echo Open PowerShell in this folder and run: py -3.12 -m pip install -r requirements.txt
    pause
    exit /b 1
)

start "Portfolio Risk API" /D "%~dp0" cmd /k "set PYTHONPATH=%~dp0backend\python&& py -3.12 -m uvicorn app.main:app --host 127.0.0.1 --port 8000"
start "Portfolio Risk Dashboard" /D "%~dp0" cmd /k "py -3.12 -m streamlit run frontend\streamlit_app.py --server.headless true --server.address 127.0.0.1 --server.port 8501"

timeout /t 4 /nobreak >nul
start "" "http://localhost:8501"
