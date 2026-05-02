# Use official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency file first
COPY requirements.txt .

# Install Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Copy full project into container
COPY . .

# Default command
CMD ["python", "-m", "src.ingest.extract_all_nasa_cycles"]