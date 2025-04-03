# Python runtime parent image
FROM python:3.10-slim

# Working directory for the container
WORKDIR /app

# Copy app contents to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for the app to listen on the port provided by Heroku
ENV PORT=5000

# Command to run the application using Gunicorn (app will start in production mode)
CMD gunicorn --bind 0.0.0.0:$PORT app:app

