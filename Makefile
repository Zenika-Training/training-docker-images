.PHONY: build-all push-all
images=k8s-training-tools k8s-training-stress securedev-training-curlbot ansible-ee-minimal

build-all:
	for image in $(images) ; do \
		cd $$image && make build && cd .. ; \
	done ; \
	cd k8s-training-deploy && make build-v1 && make build-v2

push-all:
	for image in $(images) ; do \
		cd $$image && make push  && cd .. ; \
	done ; \
	cd k8s-training-deploy && make push-v1 && make push-v2
