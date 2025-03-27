#!/bin/bash

set -o errexit
set -o nounset

celery -A app.domain.worker worker --loglevel=info
