from harrycb/python3.7torch1.5.0
copy requirements.txt .
run pip install -r requirements.txt uvicorn
copy . .
cmd uvicorn main:app --port ${PORT-8000} --host ${HOST-0.0.0.0}