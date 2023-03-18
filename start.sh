#! /usr/bin/env sh

DB_USER=${DB_ROOT_USER} DB_PASSWORD=${DB_ROOT_PASSWORD} python3 -m alembic upgrade head
cd app/
python3 -m uvicorn main:app --host 0.0.0.0
