FROM python:3.8

WORKDIR /build

COPY requirements.txt .
COPY app/ ./app
COPY .env .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]