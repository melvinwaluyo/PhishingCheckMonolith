# Gunakan base image Python
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy requirments.txt
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port yang dipakai FastAPI
EXPOSE 8000

# Jalankan FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



