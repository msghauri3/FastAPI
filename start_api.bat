@echo off
cd C:\path\to\your\fastapi\app
python -m uvicorn main:app --host 0.0.0.0 --port 8000