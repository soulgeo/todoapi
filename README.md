# Todo-list RESTful API

An API service built with the Django REST Framework for the purposes of the Software as a Service course at the University of Piraeus. Features complete unit tests and httpie tests.\
\
The application is dockerized and deployed using fly.io, and you can read its openapi-style manual here: https://todoapi-bitter-forest-5754.fly.dev/api/docs/

## How to Run

Below are instructions on how to run the application on a development environment. Docker and docker-compose are required.

1.  **Clone this repository:**
    ```bash
    git clone https://github.com/soulgeo/todoapi.git
    ```

2.  **Set up environment variables:**
    Copy the example environment file to create your local configuration:
    ```bash
    cp .env.example .env
    ```

    (You can usually leave the default values in `.env` as-is for local development with Docker.)

3.  **Start the development server:**
    Run the application using Docker Compose:
    ```bash
    docker-compose up --build
    ```

The application will be available at `http://localhost:8000`.


