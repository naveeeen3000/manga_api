FROM python:3.11.4-alpine


WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY .env.dev /app/.env

COPY . /app
RUN addgroup -S manga_app && adduser -S naveen -G manga_app
USER naveen

EXPOSE 3000
CMD ["gunicorn", "--bind", "0.0.0.0:3000", "manga_api.wsgi:application"]