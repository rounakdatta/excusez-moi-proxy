#! /usr/bin/env sh

DB_HOST=localhost DB_USER=postgres DB_PASSWORD=helloworld DB_NAME=xcuzme python3 -m alembic upgrade head
cd app/
DB_USER=postgres DB_PASSWORD=helloworld DB_NAME=xcuzme DB_HOST=localhost OPENAI_ORGANIZATION=***REMOVED*** OPENAI_API_KEY=***REMOVED*** python3 -m uvicorn main:app
