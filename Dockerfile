
FROM python:3.9-slim

#declare build arguements
ARG SECRET_KEY
ARG DB_NAME
ARG DB_USERNAME
ARG DB_PASSWORD
ARG DB_HOSTNAME
ARG DB_PORT
ARG POSTGRES_PASSWORD
ARG EMAIL_USER
ARG EMAIL_PASSWORD
ARG CELERY_BROKER_URL
ARG CELERY_RESULT_BACKEND
ARG DATABASE_URL
ARG CELERYBROKERURL
ARG CELERYRESULTBACKEND

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV SECRET_KEY=${SECRET_KEY}
ENV DB_USERNAME=${DB_USERNAME}
ENV DB_USER=${DB_USER}
ENV DB_PASSWORD=${DB_PASSWORD}
ENV DB_HOSTNAME=${DB_HOSTNAME}
ENV DB_PORT=${DB_PORT}
ENV DB_NAME=${DB_NAME}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV EMAIL_USER=${EMAIL_USER}
ENV EMAIL_PASSWORD=${EMAIL_PASSWORD}
ENV CELERY_BROKER_URL=${CELERY_BROKER_URL}
ENV CELERY_RESULT_BACKEND=${CELERY_RESULT_BACKEND}
ENV DATABASE_URL=${DATABASE_URL}
ENV CELERYBROKERURL=${CELERYBROKERURL}
ENV CELERYRESULTBACKEND=${CELERYRESULTBACKEND}

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


# Expose port 8000 (for Django)
EXPOSE 8000


# Run the Django application using Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
