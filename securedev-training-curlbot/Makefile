.PHONY: build push
image_name=ghcr.io/zenika-training/securedev-training-curlbot:v1

build:
	docker image build -t $(image_name) .

push: build
	docker image push $(image_name)

