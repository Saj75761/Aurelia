FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Cloud Run uses PORT env variable
ENV PORT=8080

EXPOSE 8080

CMD ["python", "main.py"]
