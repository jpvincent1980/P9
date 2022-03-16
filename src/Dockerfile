# syntax=docker/dockerfile:1

# Image used for our application
FROM python:3.10-slim-buster

# Creation of a working directory to be used as default path
WORKDIR /app

# Set environment variables
# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED=1
# Set port number
ENV PORT=8000

# Copying the requirements.txt file into the default path
COPY requirements.txt /app

# Run pip to install dependencies
RUN pip install -r requirements.txt

# Adding source code to the image
COPY . .

# Expose an external port
EXPOSE $PORT

# Run django server
CMD python manage.py runserver 0.0.0.0:$PORT