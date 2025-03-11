#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

alembic upgrade head
uvicorn --workers 4 --host 0.0.0.0 --port 8000 app.main:app
