FROM python:3.10

# RUN apk add --no-cache build-base
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN python3 -m pip install -U pip && python3 -m pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
COPY ./migrations /code/migrations
COPY ./alembic.ini /code/alembic.ini
COPY ./start.sh /code/start.sh
RUN chmod +x /code/start.sh

CMD ["/code/start.sh"]
