.PHONY: install freeze build run stop clean ps logs
SHELL := /bin/bash

# Define variables
IMAGE_NAME = hire-match-app
CONTAINER_NAME = hire-match-container
PORT = 8000

# Install dependencies
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt

# Freeze dependencies into requirements.txt

freeze:
	pip freeze > requirements.txt

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run -d -p $(PORT):8000 --name $(CONTAINER_NAME) $(IMAGE_NAME)

# Stop the running container
stop:
	docker stop $(CONTAINER_NAME) || true

# Remove the container
clean:
	docker rm $(CONTAINER_NAME) || true
	docker rmi $(IMAGE_NAME) || true

# View running containers
ps:
	docker ps

# Show logs from the container
logs:
	docker logs -f $(CONTAINER_NAME)
