FROM python:3.12-slim-bookworm

# Install ffmpeg and other dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd -m -u 1000 app

# Set up working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership of the app directory to the non-root user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose the port Gradio runs on
EXPOSE 7860

# Set environment variable for Gradio to listen on all interfaces
ENV GRADIO_SERVER_NAME=0.0.0.0

# Command to run the application
CMD ["python", "main.py"]
