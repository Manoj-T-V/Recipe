# Recipe API

This is an API for managing recipes, users, and related functionalities. The API is built with Django, Django REST Framework, and PostgreSQL, and it uses Celery and Redis for background tasks.

## Features
- Recipe management: create, update, delete, and view recipes with optimised querysets.
- Recipe likes and user bookmarks.
- Email queue to send notifications asynchronously,including a daily notification to authors about the likes received on their recipes.
- User authentication and registration with optimised querysets.
- test cases for all APIs and generate a coverage report.
- Containerized the application

## Technologies Used
- **Backend**: Django, Django REST Framework
- **Task Queue**: Celery with Redis as the broker
- **Database**: PostgreSQL
- **Containerization**: Docker and Docker Compose
- **API Documentation**: drf-spectacular (Swagger UI)

## Live Version
The live version of the application is hosted on Render <https://recipe-api-oyib.onrender.com/>


## Table of Contents
- Features
- Technologies Used
- Live Version
- Getting Started
- Installation
  - Option 1: Clone the Repository and Build Locally
  - Option 2: Use Pre-built Docker Images
- CI/CD
- Running Tests
- Scaling the Service

## Getting Started

### Prerequisites
- Python 
- PostgreSQL 
- Redis 
- Docker and Docker Compose.



### Installation

#### Option 1: Clone the Repository and Build Locally

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/recipe-api.git
    cd recipe-api
    ```
2. **Setup local or Hosted Postgres and Redis**:
   Ensure you have Connection strings/urls for Postgres and Redis to connect from local:


3. **Create a `.env` File**:
   Create a `.env` file in the root directory of the project and add all the necessary environment variables including mail credentials. Example:

    ```env
    SECRET_KEY=your_secret_key  # Django secret key
    DATABASE_URL=your_database_url  # PostgreSQL database URL
    CELERY_BROKER_URL=your_redis_url  # Redis URL for Celery
    ```
4. **Install Python Modules**:
   Ensure you have `pip` installed, then install the necessary Python modules from `requirements.txt`:

    ```bash
    pip install -r requirements.txt
    ```
5. **Apply Migrations**:

    ```bash
    python manage.py migrate
    ```
6. **Create a Superuser: Create a superuser to access the Django admin panel:**:

    ```bash
    python manage.py migrate
    ```
7. **Run Celery Worker and Beat: Open two separate terminal windows or tabs and run the following commands:**:

    ```bash
    celery -A project_name worker --loglevel=info
    celery -A project_name beat --loglevel=info
    ```

8. **Access the Application**:
    - Admin Panel: http://localhost:8000/admin/
    - API Swagger UI: http://localhost:8000/

#### Option 2: Use Pre-built Docker Images

1. **Pull Docker Images**:
    If you prefer to use pre-built Docker images from Docker Hub:

    ```bash
    docker pull manojtv/myapp-web:latest
    docker pull manojtv/myapp-celery:latest
    docker pull manojtv/myapp-celery-beat:latest
    ```

2. **Create a `docker-compose.override.yml` File**:
   Create a `docker-compose.override.yml` file in the root directory and specify the images and environment variables  Example:

    ```yaml
    version: '3'
    services:
      web:
        image: manojtv/myapp-web:latest
        environment:
          - DATABASE_URL=your_database_url
          - SECRET_KEY=your_secret_key
          - CELERY_BROKER_URL=your_redis_url
      celery:
        image: manojtv/myapp-celery:latest
        environment:
          - CELERY_BROKER_URL=your_redis_url
      celery-beat:
        image: manojtv/myapp-celery-beat:latest
        environment:
          - CELERY_BROKER_URL=your_redis_url
    ```

3. **Run the Containers**:
    Start the Docker containers using Docker Compose:

    ```bash
    docker-compose up
    ```

4. **Run Migrations**:

    ```bash
    docker-compose exec web python manage.py migrate
    ```

5. **Create a Superuser and start celery workers and beat schedulers**:

    ```bash
    docker-compose exec web python manage.py createsuperuser
    docker-compose exec celery celery -A your_project_name worker --loglevel=info
    docker-compose exec celery-beat celery -A your_project_name beat --loglevel=info
    ```

6. **Access the Application on the host port specified**:
    - Admin Panel: http://localhost:8080/admin/
    - API Swagger UI: http://localhost:8080/


## CI/CD with GitHub Actions

This setup ensures that any code changes pushed to the `master` branch will automatically trigger a new Docker image build in the Docker Hub and redeploy the web service on Render using the new image. This maintains a seamless and automated CI/CD pipeline for application. 


## Running Tests

To run tests and check coverage, follow these steps:

2. **Run Tests with Coverage**:
    Ensure you have `pytest` and `pytest-cov` installed:

    ```bash
    pip install pytest pytest-cov pytest-django
    ```

    Then, run the tests with coverage and generate a coverage report, replace recipe with user for user testing:

    ```bash
    docker-compose exec web pytest --cov=recipe --cov-report=html
    pytest --cov=recipe --cov-report=html
    ```

    - **`--cov=recipe`**: Measures coverage for the `recipe` module.
    - **`--cov-report=html`**: Generates an HTML report of the coverage results, saved in the `htmlcov` directory.

2. **View Coverage Report**:
    Open the generated HTML report in a web browser: Currently this application test coverage is not 100 percent.

    ```bash
    open htmlcov/index.html
    ```
## Scaling the Service

To scale your services, you can adjust the number of replicas for your Docker services. Here are some examples for scaling different services:

1. **Scaling All Services**:
   You can scale multiple services individually or simultaneously:

    ```bash
    docker-compose up --scale web=3 --scale celery=3 --scale celery-beat=2
    ```

    This command will start three instances of the `web` service, three instances of the `celery` service, and two instances of the `celery-beat` service.

2. **Scale Celery Processes**:
   If you are using multiple Celery processes (e.g., for different types of tasks), you can configure your `celery` service to start with multiple processes. Adjust the `CELERY_WORKER_CONCURRENCY` setting in your Celery configuration:

    ```bash
    celery -A your_project_name worker --concurrency=4
    ```

    Replace `4` with the desired number of processes. You might need to modify the `celery` service definition in your `docker-compose.yml` to pass this argument.



