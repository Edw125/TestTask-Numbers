FROM python:3.7-slim

ADD start.sh /

RUN chmod +x /start.sh

RUN mkdir /app

COPY ./TestTask/requirements.txt /app

RUN python -m pip install --upgrade pip

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY ./TestTask /app

WORKDIR /app

CMD ["/start.sh"]
