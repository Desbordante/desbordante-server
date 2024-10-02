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

1. Run server application
2. Open https://localhost:8000/docs

## License

Distributed under the GNU AGPL v3.
See [LICENSE](LICENSE) for more information.
