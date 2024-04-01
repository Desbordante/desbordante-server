.PHONY: env install-deps up open-db revision migrate downgrade worker app init lint test

ifeq ($(shell test -e '.env' && echo -n yes), yes)
	include .env
endif

args := $(wordlist 2, 100, $(MAKECMDGOALS))

## Create .env file from .env.example
env:
	@cp .env.example .env
	@echo >> .env
	@echo "SECRET_KEY=$$(openssl rand -hex 32)" >> .env

## Install dependencies
install-deps:
	poetry install
	poetry run pre-commit install

## Up development-only docker containers
up:
	(trap 'docker compose -f dev-docker-compose.yaml down' INT; \
	docker compose -f dev-docker-compose.yaml up --build --force-recreate --remove-orphans $(args))

## Open database with docker-compose
open-db:
	docker exec -it desbordante-postgres psql -d $(POSTGRES_DB) -U $(POSTGRES_USER)

## Create new revision file automatically
revision:
	poetry run alembic -c app/settings/alembic.ini revision --autogenerate $(args)

## Make migrations in database
migrate:
	poetry run alembic -c app/settings/alembic.ini upgrade $(args)

## Downgrade database
downgrade:
	poetry run alembic -c app/settings/alembic.ini downgrade $(args)

## Run celery worker in watch mode
worker:
	watchmedo auto-restart --directory=./ --pattern='*.py' --recursive -- celery -A app.worker worker --loglevel=info --concurrency=1

## Run application server in watch mode
app:
	poetry run uvicorn --port 8000 app.main:app --reload

## Initiate repository
init:
	make env install-deps

## Run all formatters and linters in project
lint:
	poetry run ruff check tests app \
	& poetry run ruff format --check tests app \
	& poetry run black --check tests app

## Reformat code
format:
	poetry run ruff format tests app & poetry run ruff check --fix & poetry run black tests app


## Run all tests in project
test:
	poetry run pytest -o log_cli=true --verbosity=2 --showlocals --log-cli-level=INFO --cov=app --cov-report term

.DEFAULT_GOAL := help
# See <https://gist.github.com/klmr/575726c7e05d8780505a> for explanation.
help:
	@echo "$$(tput setaf 2)Available rules:$$(tput sgr0)";sed -ne"/^## /{h;s/.*//;:d" -e"H;n;s/^## /---/;td" -e"s/:.*//;G;s/\\n## /===/;s/\\n//g;p;}" ${MAKEFILE_LIST}|awk -F === -v n=$$(tput cols) -v i=4 -v a="$$(tput setaf 6)" -v z="$$(tput sgr0)" '{printf"- %s%s%s\n",a,$$1,z;m=split($$2,w,"---");l=n-i;for(j=1;j<=m;j++){l-=length(w[j])+1;if(l<= 0){l=n-i-length(w[j])-1;}printf"%*s%s\n",-i," ",w[j];}}'
