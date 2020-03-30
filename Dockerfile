FROM python:3.7
COPY requirements.txt .
RUN pip install -r requirements.txt uvicorn
COPY . .
CMD uvicorn main:app --port ${PORT-8000} --host 0.0.0.0