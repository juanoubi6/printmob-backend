FROM python:3.7-slim

COPY . /app
WORKDIR /app

RUN chmod -R 777 ./bin/entrypoint.sh
RUN pip install --no-cache-dir .

# tzdata for timzone
RUN apt-get update -y
RUN apt-get install -y tzdata
ENV TZ America/Argentina/Buenos_Aires

ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y binutils libc-dev

ENTRYPOINT ["sh", "bin/cronjobs-entrypoint.sh"]
