@echo off
SETLOCAL

REM Handle input arguments
IF "%~1"=="" (
    SET FIRST_PAGE=1
    SET LAST_PAGE=10
) ELSE IF "%~2"=="" (
    SET FIRST_PAGE=1
    SET LAST_PAGE=%1
) ELSE (
    SET FIRST_PAGE=%1
    SET LAST_PAGE=%2
)

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

echo Running main script with FIRST_PAGE=%FIRST_PAGE% and LAST_PAGE=%LAST_PAGE% ...
python -m src.Runner.parallel %FIRST_PAGE% %LAST_PAGE%

ENDLOCAL
