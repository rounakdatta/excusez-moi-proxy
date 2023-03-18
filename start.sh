#! /usr/bin/env sh

python3 -m alembic upgrade head
cd app/
python3 -m uvicorn main:app
