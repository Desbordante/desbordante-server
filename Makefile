.PHONY: env volumes install-deps up open-db pg-revision pg-migrate pg-downgrade celery-worker app init lint test check-types

ifeq ($(shell test -e '.env' && echo -n yes), yes)
	include .env
endif

args := $(wordlist 2, 100, $(MAKECMDGOALS))

## Create .env file from .env.example
env:
	@cp .env.example .env
	@echo >> .env
	@echo "SECRET_KEY=$$(openssl rand -hex 32)" >> .env

## Create folders for volumes
volumes:
	@for volume in postgres rabbitmq uploads; do \
    	mkdir -p ./volumes/$$volume; \
    	chmod 777 ./volumes/$$volume; \
    done

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
pg-revision:
	poetry run alembic -c internal/infrastructure/data_storage/relational/postgres/migrations/alembic.ini revision --autogenerate $(args)

## Make migrations in database
pg-migrate:
	poetry run alembic -c internal/infrastructure/data_storage/relational/postgres/migrations/alembic.ini upgrade $(args)

## Downgrade database
pg-downgrade:
	poetry run alembic -c internal/infrastructure/data_storage/relational/postgres/migrations/alembic.ini downgrade $(args)

## Run celery worker in watch mode
celery-worker:
	poetry run watchmedo auto-restart --directory=./ --pattern='*.py' --recursive -- celery -A internal.infrastructure.background_task.celery worker --loglevel=info --concurrency=1

## Run application server in watch mode
app:
	poetry run uvicorn --port 8000 internal:app --reload

## Initiate repository
init:
	make env volumes install-deps

## Run all formatters and linters in project
lint:
	poetry run ruff check tests internal \
	& poetry run ruff format --check tests internal

## Reformat code
format:
	poetry run ruff format tests internal & poetry run ruff check --fix

## Run all tests in project
test:
	poetry run pytest -o log_cli=true --verbosity=2 --showlocals --log-cli-level=INFO --cov=internal --cov-report term

## Check all types
check-types:
	poetry run pyright .

.DEFAULT_GOAL := help
# See <https://gist.github.com/klmr/575726c7e05d8780505a> for explanation.
help:
	@echo "$$(tput setaf 2)Available rules:$$(tput sgr0)";sed -ne"/^## /{h;s/.*//;:d" -e"H;n;s/^## /---/;td" -e"s/:.*//;G;s/\\n## /===/;s/\\n//g;p;}" ${MAKEFILE_LIST}|awk -F === -v n=$$(tput cols) -v i=4 -v a="$$(tput setaf 6)" -v z="$$(tput sgr0)" '{printf"- %s%s%s\n",a,$$1,z;m=split($$2,w,"---");l=n-i;for(j=1;j<=m;j++){l-=length(w[j])+1;if(l<= 0){l=n-i-length(w[j])-1;}printf"%*s%s\n",-i," ",w[j];}}'
