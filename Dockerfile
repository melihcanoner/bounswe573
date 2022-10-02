FROM python:3.8-alpine
LABEL maintainer="Melih Can Oner"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

RUN apk update
RUN apk add --update  --no-cache postgresql-client jpeg-dev libffi-dev gcc vim

RUN apk add --update  --no-cache --virtual .tmp-build-deps \
      libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

EXPOSE 8000
ENV LC_ALL=en_US.UTF8

RUN mkdir /app

WORKDIR /app

COPY ./app /app

RUN mkdir -p /app/media
RUN mkdir -p /app/static
RUN adduser -D user
RUN chown -R user:user /app/
RUN chmod 755 /app/

USER user
