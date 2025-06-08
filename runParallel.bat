@echo off
SETLOCAL
SET TOTAL_PAGES=%1
IF "%TOTAL_PAGES%"=="" SET TOTAL_PAGES=10

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

echo Running main script with TOTAL_PAGES=%TOTAL_PAGES% ...
python -m src.Runner.parallel %TOTAL_PAGES%

ENDLOCAL
