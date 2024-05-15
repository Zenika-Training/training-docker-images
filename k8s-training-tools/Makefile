.PHONY: build push
image_name=zenika/k8s-training-tools:v5

build:
	docker image build -t $(image_name) .

push: build
	docker image push $(image_name)
