FROM debian:stretch

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-dev

COPY ./requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT ["python3"]
CMD ["run.py"]
