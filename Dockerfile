# Python runtime parent image
FROM python:3.10-slim

# Working directory for the container
WORKDIR /app

# Copy the app contents to the container
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 3000

# Command to run the application
CMD ["python", "app.py"]