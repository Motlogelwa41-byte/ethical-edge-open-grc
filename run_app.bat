@echo off
echo 🚀 Starting Ethical Edge GRC Platform...

:: Step 1: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python to continue.
    pause
    exit /b
)

:: Step 2: Install/Update dependencies
echo 📦 Checking for missing libraries...
pip install -r requirements.txt

:: Step 3: Run the Application
echo 🌐 Server starting at http://127.0.0.1:5000
echo 🛡️  Pillars Active: Governance, Risk
python -m app.main

pause
