FROM debian:11-slim

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
            stress \
    ; \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["stress"]
