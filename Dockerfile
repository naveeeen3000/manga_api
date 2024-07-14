FROM python:3.11.4-alpine


WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache \
    mariadb-connector-c-dev \
    gcc \
    musl-dev \
    linux-headers

RUN pip3 install --upgrade pip
RUN python3 -m venv env
RUN source env/bin/activate
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY . /app
RUN addgroup -S manga_app && adduser -S naveen -G manga_app
USER naveen

EXPOSE 3000
CMD ["gunicorn", 
"--bind", "0.0.0.0:3000", 
"--workers", "4",
"--worker-class", "gthread", 
"--threads", "2",
"--log-level", "INFO",
"--log-file", "/var/log/manga/log_manga.log",
"--access-logfile", "/var/log/manga/manga_access.log",
"manga_api.wsgi:application"]