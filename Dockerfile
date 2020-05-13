FROM python:3.8.2-slim

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

COPY . /app
WORKDIR /app
EXPOSE 80
CMD [ "bash", "docker_run.sh" ]
