# Desbordante

## Installation

1. Required `python3.12` or newer
2. Install [poetry](https://python-poetry.org/) — dependency management tool
3. Install dependencies: `make init`

## Local development

Execute `make` to see all available rules with documentation

1. Activate virtual environment: `source .venv/bin/activate`
2. Don't forget to change values in .env
3. Run **development-only** containers: `make up`
4. Run celery worker in watch mode: `make celery-worker`
5. Run application in watch mode: `make app`

## Docs

1. Run the server application
2. Access the following documentation and monitoring interfaces on `localhost`:
   - **FastAPI documentation (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Flower Celery monitoring panel:** [http://localhost:5555](http://localhost:5555)


## License

Distributed under the GNU AGPL v3.
See [LICENSE](LICENSE) for more information.
