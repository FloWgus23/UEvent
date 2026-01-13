# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

# Copy all project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port (Railway will use $PORT)
EXPOSE 8000

# Start gunicorn server
CMD gunicorn uevent.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --log-file - --access-logfile - --error-logfile -