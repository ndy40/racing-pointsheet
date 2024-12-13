#!/usr/bin/env sh

set -e


param=$1


docker compose exec -it backend python main.py "$@"
