# Desbordante server

## Installation

1. Required `python3.13` or newer
2. Install [uv](https://docs.astral.sh/uv/) — Python package and project manager,
3. Install dependencies: `make init`

## Local development

Execute `make` to see all available rules with documentation

1. Don't forget to change values in `.env`
2. Run app and services in dev mode: `make dev`

## Docs

1. Run the server application
2. Access the following documentation and monitoring interfaces on `localhost`:
   - **FastAPI documentation (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Flower Celery monitoring panel:** [http://localhost:5555](http://localhost:5555)


## License

Distributed under the GNU AGPL v3.
See [LICENSE](LICENSE) for more information.
