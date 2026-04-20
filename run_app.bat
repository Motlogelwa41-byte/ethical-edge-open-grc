@echo off
echo 🚀 Starting Ethical Edge GRC Platform...
SET PYTHONPATH=.

:: Step 1: Use 'py' launcher instead of 'python'
echo 📦 Checking for missing libraries...
py -m pip install -r requirements.txt

:: Step 2: Run the Application using the 'py' module path
echo 🌐 Server starting at http://127.0.0.1:5000
echo 🛡️ Pillars Active: Governance, Risk
py app/main.py

pause
