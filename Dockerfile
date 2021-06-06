FROM python:3.7-slim

COPY . /app
WORKDIR /app

RUN chmod -R 777 ./bin/entrypoint.sh
RUN pip install --no-cache-dir .

RUN apt-get update && apt-get install -y binutils libc-dev

ENTRYPOINT ["sh", "bin/entrypoint.sh"]
