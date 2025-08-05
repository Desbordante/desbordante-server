#!/bin/bash

set -o errexit
set -o nounset

celery -A src.worker worker -B --loglevel=info
