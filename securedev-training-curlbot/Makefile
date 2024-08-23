.PHONY: build-v1 push-v1 build-v2 push-v2 build push
image_name=ghcr.io/zenika-training/securedev-training-curlbot

build-v1: version=v1
build-v1: build

push-v1: version=v1
push-v1: build push

build-v2: version=v2
build-v2: build

push-v2: version=v2
push-v2: build push

build:
	docker image build --build-arg VERSION=$(version) -t $(image_name):$(version) .

push:
	docker image push $(image_name):$(version)
