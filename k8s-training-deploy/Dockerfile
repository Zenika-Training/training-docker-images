FROM gcr.io/distroless/python3

ARG VERSION=v0

ENV VERSION=${VERSION}

ADD app.py /app.py

ENTRYPOINT ["python3", "-u", "/app.py"]
