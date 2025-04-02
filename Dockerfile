# Python runtime parent image
FROM python:3.10-slim

# Working directory for the container
WORKDIR /app

# Copy app contents to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the app will run on
EXPOSE 5000

# Command to run the application using Gunicorn (app will start in production mode)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
