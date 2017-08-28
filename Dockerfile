FROM python:3.5.4

COPY . /
WORKDIR /

RUN pip3 install -r requirements.txt

CMD python -m main.src.server.service 80
