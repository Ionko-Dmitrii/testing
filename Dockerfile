FROM python:3.9
RUN mkdir /web_django
WORKDIR /web_django

COPY requirements.txt /web_django
RUN pip install -r requirements.txt
COPY . .
RUN chmod +x /web_django/docker-entrypoint.sh
