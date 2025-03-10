.PHONY: env install list format app services dev

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
install:
	uv sync
	uv run pre-commit install

## Initiate repository
init:
	make env install

## Run linters
lint:
	uv run ruff check

## Reformat code
format:
	uv run ruff format

## Run application server in watch mode
app:
	uv run uvicorn --port 8000 app.main:app --reload

## Run development-only docker containers
services:
	(trap 'docker compose -f dev-docker-compose.yaml down' INT; \
	docker compose -f dev-docker-compose.yaml up -d --build --force-recreate --remove-orphans $(args))

## Run app and services in dev mode
dev:
	make services
	make app

.DEFAULT_GOAL := help
# See <https://gist.github.com/klmr/575726c7e05d8780505a> for explanation.
help:
	@echo "$$(tput setaf 2)Available rules:$$(tput sgr0)";sed -ne"/^## /{h;s/.*//;:d" -e"H;n;s/^## /---/;td" -e"s/:.*//;G;s/\\n## /===/;s/\\n//g;p;}" ${MAKEFILE_LIST}|awk -F === -v n=$$(tput cols) -v i=4 -v a="$$(tput setaf 6)" -v z="$$(tput sgr0)" '{printf"- %s%s%s\n",a,$$1,z;m=split($$2,w,"---");l=n-i;for(j=1;j<=m;j++){l-=length(w[j])+1;if(l<= 0){l=n-i-length(w[j])-1;}printf"%*s%s\n",-i," ",w[j];}}'
