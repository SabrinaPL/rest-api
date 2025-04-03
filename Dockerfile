# Python runtime parent image
FROM python:3.10-slim

# Working directory for the container
WORKDIR /app

# Copy app contents to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application using Gunicorn (app will start in production mode)
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:$PORT"]
