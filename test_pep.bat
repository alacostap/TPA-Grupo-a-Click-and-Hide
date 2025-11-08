@echo off
echo "PEP Errors"

flake8 . --max-line-length=100 --exclude .venv,venv,build,dist,.git,__pycache__,migrations