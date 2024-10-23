#!/bin/bash

set -o errexit
set -o nounset

worker_ready() {
    celery -A internal.infrastructure.background_task.celery inspect ping
}

until worker_ready; do
  >&2 echo 'Celery workers not available'
  sleep 1
done
>&2 echo 'Celery workers is available'

celery \
    --app=internal.infrastructure.background_task.celery \
    flower \
    --port=5555
    --basic-auth=${FLOWER_USER}:${FLOWER_PASSWORD}