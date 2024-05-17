.PHONY: build push
image_name=ghcr.io/zenika-training/k8s-training-stress:v3

build:
	docker image build -t $(image_name) .

push: build
	docker image push $(image_name)
