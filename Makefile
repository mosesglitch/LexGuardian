# Variables
IMAGE_NAME := lexguardian
IMAGE_TAG := latest
DOCKER_REPO := kimani007

# Phony targets
.PHONY: build run push clean all

# Default target
all: build

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) .

# Run the Docker container
run:
	docker run -p 8501:8501 $(IMAGE_NAME):$(IMAGE_TAG)

# Push the image to a Docker repository
push:
	docker tag $(IMAGE_NAME):$(IMAGE_TAG) $(DOCKER_REPO)/$(IMAGE_NAME):$(IMAGE_TAG)
	docker push $(DOCKER_REPO)/$(IMAGE_NAME):$(IMAGE_TAG)

# Pull the image from a Docker repository
pull:
	docker pull $(DOCKER_REPO)/$(IMAGE_NAME):$(IMAGE_TAG)

# Clean up Docker images
clean:
	docker rmi $(IMAGE_NAME):$(IMAGE_TAG)
	docker rmi $(DOCKER_REPO)/$(IMAGE_NAME):$(IMAGE_TAG)

# Build and run
build-and-run: build run

# Build and push
build-and-push: build push

# Pull and run
pull-and-run: pull run
