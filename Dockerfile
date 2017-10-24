FROM debian:stretch

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-dev cron python3-psycopg2


COPY crontab /etc/cron.d/clanner-task
RUN chmod 0644 /etc/cron.d/clanner-task
RUN service cron start

COPY ./requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

RUN chmod +x /app/run.sh
CMD ["/app/run.sh"]
