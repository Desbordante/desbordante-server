# Desbordante

## Installation

1. Required `python3.11` or newer
2. Install [poetry](https://python-poetry.org/) — dependency management tool
3. Install dependencies: `poetry install`
4. (!) Install pre-commit hooks: `poetry run pre-commit install`
5. Run server application: `poetry run uvicorn --port 8000 app.main:app`

## Local development

1. Activate virtual environment: `source .venv/bin/activate`
2. Up RabbitMQ and PostgresQL: `docker compose up --build --force-recreate`
3. Run server with reload on save: `uvicorn --port 8000 app.main:app --reload`
4. Run celery worker with reload on
   save: `watchmedo auto-restart --directory=./ --pattern='*.py' --recursive -- celery -A app.worker worker --loglevel=info --concurrency=1`

## Docs

1. Run server application
2. Open https://localhost:8000/docs

## License

Distributed under the GNU AGPL v3.
See [LICENSE](LICENSE) for more information.
