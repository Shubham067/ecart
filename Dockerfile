# pull official base image
FROM python:3.9.7-slim-buster

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential zlib1g-dev git curl bash \
    && apt-get clean

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install wheel && pip install -r requirements.txt

# copy project
COPY . .

RUN mkdir ./logs
RUN touch ./logs/gunicorn.log
RUN touch ./logs/gunicorn-access.log
RUN chmod 666 ./logs/gunicorn.log
RUN chmod 666 ./logs/gunicorn-access.log

# add and run as non-root user
RUN adduser --disabled-password myuser
USER myuser

EXPOSE 8000

# run gunicorn
CMD ["gunicorn", "--bind", ":8000", "--workers", "1", "ecommerce.wsgi:application", "--log-level", "debug", "--log-file", "./logs/gunicorn.log", "--access-logfile", "./logs/gunicorn-access.log"]