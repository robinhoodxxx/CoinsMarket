@echo off
SETLOCAL

REM Check if dependencies were installed
IF NOT EXIST "venv_done.txt" (
    echo Installing dependencies...
    pip install -r req.txt
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to install dependencies.
        EXIT /B 1
    )
    echo done > venv_done.txt
)

echo Running main script with TOTAL_PAGES=%1...
python -m src.Runner.parallel %1

ENDLOCAL
