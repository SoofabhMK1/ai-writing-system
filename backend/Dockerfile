# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the application code
COPY ./app /app/app

# Change the owner of the files to the app user
RUN chown -R app:app /app

# Switch to the non-root user
USER app

# The command to run the application will be specified in docker-compose.yml
