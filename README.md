# ProjectX

python -m venv .venv
pip install -r .\api\requirements.txt
uvicorn app.main:app --reload --app-dir API
