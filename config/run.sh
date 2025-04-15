#!/bin/bash

export PYTHONPATH=$(pwd)

cd src/database/ && poetry run alembic upgrade heads

cd ../.. && poetry run python -m src
