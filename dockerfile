# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy only the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables for Uvicorn configuration
ENV UVICORN_HOST=0.0.0.0
ENV UVICORN_PORT=8000
ENV UVICORN_WORKERS=5

# Run the application
CMD uvicorn src.main:app --host $UVICORN_HOST --port $UVICORN_PORT --workers $UVICORN_WORKERS
