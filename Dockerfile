# Pull official base image
FROM python:3.12-slim-bullseye

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . .

# Run gunicorn
# CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
# For dev/teaching purposes, we often use managed runserver in entrypoint or manual cmd, 
# but for production plan we should use gunicorn. For now, let's keep it simple or standard.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
