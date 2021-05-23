FROM python:3.7

WORKDIR /usr/src/app

COPY setup.py ./
COPY README.md ./
RUN pip install --no-cache-dir .

RUN apt-get update && apt-get install -y binutils libc-dev

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]
