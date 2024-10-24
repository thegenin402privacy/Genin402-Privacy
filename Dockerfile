FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY genin402/ ./genin402/
EXPOSE 8000
CMD ["uvicorn", "genin402.server:app", "--host", "0.0.0.0", "--port", "8000"]
