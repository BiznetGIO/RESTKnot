FROM python:3.7-alpine

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN apk update && \
    # need these depedencies in order for psycopg2 to be installed via pip
    apk --no-cache add gcc linux-headers postgresql-dev musl-dev && \
    pip3 install -r requirements.txt && \
    pip3 install gunicorn

EXPOSE 5000
CMD ["gunicorn", "app:create_app()", "-b", "0.0.0.0:5000"]
