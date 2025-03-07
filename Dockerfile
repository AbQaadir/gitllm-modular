# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create a non-root user with UID 10016 as required by Choreo
RUN groupadd -g 10016 choreo && \
    useradd --uid 10016 --gid 10016 --no-create-home --shell /bin/bash choreouser

# Switch to the non-root user
USER 10016

# Expose the port specified in component.yaml (8000)
EXPOSE 8000

# Command to run the FastAPI application with Uvicorn
CMD ["python", "main.py"]