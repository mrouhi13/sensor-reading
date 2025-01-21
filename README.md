## Sensor Reading
#### Einhundert Case Study

This is a Django-based RESTful API for reading sensors data.

## Features
- CRUD actions for sensor reading via RestAPI.
- Fetch sensor readings data from external api using background tasks.

### Prerequisites

- Docker and docker compose installed on your machine

### Running

1. **Clone the repository**:
    ```bash
    git clone https://github.com/mrouhi13/sensor-reading.git
    cd sensor-reading
    ```

2. **Environment Variables**:
    Make sure to set the following environment variables in a `.env` file:
    ```
    WEB_API_DOMAIN=0.0.0.0

    SECRET_KEY=dummy_secret_key

    DJANGO_ENV=dev

    REDIS_HOST=redis://redis:6379

    POSTGRES_DB=postgres
    POSTGRES_HOST=postgres
    POSTGRES_PORT=5432
    POSTGRES_PASSWORD=postgres
    POSTGRES_USER=postgres
    ```

3. **Run the server**:
    ```bash
    docker compose -p sr up --build -d
    ```

4. **Check services status**:
    ```bash
    docker compose -p sr ps
    ```

5. **Accessing the Documentation**:
     - **Swagger UI**: [http://localhost:8000/docs/swagger/](http://localhost:8000/docs/swagger/)
     - **OpenAPI JSON**: [http://localhost:8000/schema/](http://localhost:8000/schema/)

### Testing

1. **Run tests and coverage**:
    ```bash
    docker compose -p sr exec -e DJANGO_ENV=test app pytest source/
    ```

2. **Check code style**:
    ```bash
    docker compose -p sr exec app ruff check source/
    ```
