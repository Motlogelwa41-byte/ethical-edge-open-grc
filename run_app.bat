@echo off
echo Starting Ethical Edge GRC Engine...
source venv/Scripts/activate
uvicorn app.main:app --reload
pause
