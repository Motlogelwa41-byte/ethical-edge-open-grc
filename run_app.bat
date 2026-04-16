@echo off
echo Starting Ethical Edge GRC Engine...
:: Activate the virtual environment (Windows style)
call venv\Scripts\activate
:: Run the application using Python's module mode to avoid "command not found"
python -m uvicorn app.main:app --reload
pause
