FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["fastapi", "dev", "app/main.py", "--host", "0.0.0.0", "--port", "8080"]