.PHONY: cleanup create build_with_podman
image_name=ghcr.io/zenika-training/ansible-ee-minimal:2.17.14

cleanup:
	rm -rf _build
	rm -f Dockerfile

create:
	ansible-builder create -f execution-environment.yml -c . --output-filename Dockerfile

build_with_podman:
	podman build --no-cache -f Dockerfile . -t $(image_name)

show_version_with_podman:
	podman run --rm -ti --name runner $(image_name) ansible --version 
	podman run --rm -ti --name runner $(image_name) ansible-galaxy collection list

build:
	docker image build -t $(image_name) .

push: build
	docker image push $(image_name)