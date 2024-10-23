#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

alembic -c internal/infrastructure/data_storage/relational/postgres/migrations/alembic.ini upgrade head
uvicorn --workers 1 --host 0.0.0.0 --port $APPLICATION_SERVER_PORT internal:app