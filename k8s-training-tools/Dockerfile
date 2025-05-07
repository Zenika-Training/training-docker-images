FROM debian:12-slim

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
            curl \
            dnsutils \
            iputils-ping \
            iproute2 \
            httping \
            procps \
            ca-certificates \
            vim \
    ; \
    rm -rf /var/lib/apt/lists/*

ENV JWT_VERSION=6.0.0
RUN curl -fSsLO https://github.com/mike-engel/jwt-cli/releases/download/${JWT_VERSION}/jwt-linux.tar.gz && \
    tar zxf jwt-linux.tar.gz && \
    rm /jwt-linux.tar.gz && \
    mv jwt /usr/bin

ENV KUBECTL_VERSION=v1.33.0
RUN curl -fsSLo /usr/local/bin/kubectl https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/arm64/kubectl \
  && chmod +x /usr/local/bin/kubectl
