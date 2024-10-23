#!/bin/bash

set -o errexit
set -o nounset

celery -A internal.infrastructure.background_task.celery worker --loglevel=info