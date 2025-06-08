@echo off
IF NOT EXIST "venv_done.txt" (
    echo Installing dependencies...
    pip install -r req.txt
    echo done > venv_done.txt
)

echo Running main script...
python -m src.Runner.parallel

