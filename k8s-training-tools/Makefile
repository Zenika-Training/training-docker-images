.PHONY: build push
image_name=ghcr.io/zenika-training/k8s-training-tools:v6

build:
	docker image build -t $(image_name) .

push: build
	docker image push $(image_name)
