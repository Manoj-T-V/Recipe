
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /recipe-api

# Install dependencies
COPY requirements.txt /recipe-api/

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /recipe-api/

# Collect static files
RUN python manage.py collectstatic --noinput


# Expose port 8000 (for Django)
EXPOSE 8000


# Run the Django application using Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
