#!/bin/bash

export PYTHONPATH=$(pwd)

cd src/infrastructure/db/ && poetry run alembic upgrade heads

cd ../../.. && poetry run python -m src
