# Use an official Python runtime as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Copy the application files to the working directory
COPY requirements.txt /app/
COPY app.py /app/
COPY server_llm.py /app/
COPY .env /app/
COPY faiss_index/ /app/faiss_index/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port (FastAPI default: 8000)
EXPOSE 8000

# Run the FastAPI application using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]