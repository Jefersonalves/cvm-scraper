FROM python:3.7

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y libpq-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD "python -m http.server"