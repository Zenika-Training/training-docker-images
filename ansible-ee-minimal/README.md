# Optimized Execution Environments for Ansible and AWX Training

Ansible and AWX training courses greatly benefit from customized execution environments (EEs). 
Default images, like the AWX one (nearly 2 GB), pose problems with size, superfluous dependencies, and lengthy loading times.

A default EE image is often too large for training deployments, weighed down by unnecessary collections that slow down downloads and startup.

The advantage of a lightweight and targeted EE is clear: an image of only 500 MB drastically reduces disk footprint, accelerates loading, and ensures a stable, relevant, and controlled environment for practical labs. 
We only keep what's essential, making training smoother and more effective.

To generate the Dockerfile (the `ansible-builder` tool is required) from `execution-environment.yml`:

```bash
make cleanup create
```

To build the container with Podman:

```bash
make build_with_podman
```

To display the execution environment versions with Podman:

```bash
make show_version_with_podman
```

To build the container with Docker:

```bash
make build
```