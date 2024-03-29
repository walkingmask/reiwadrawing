FROM python:3.9.5-buster as builder

ADD requirements.txt /tmp/requirements.txt
RUN pip install -U pip
RUN pip install -r tmp/requirements.txt

FROM python:3.9.4-slim-buster

COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn