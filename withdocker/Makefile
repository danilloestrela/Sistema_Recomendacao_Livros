.PHONY: help init build

help:
	@echo "Available commands:"
	@echo "  make           - Show this help message"
	@echo "  make up        - Start the project with Docker Compose"
	@echo "  make configure - Create Python venv and install requirements (host, optional)"
	@echo "  make down      - Stop and remove Docker containers"
	@echo "  make shell     - Open a shell in the running Docker container"
	@echo "  make destroy   - Remove __pycache__, all generated files, Docker images, and volumes"

up:
	docker compose up -d

shell:
	docker compose run --rm app /bin/sh

configure:
	@if [ ! -d venv ]; then \
		python3 -m venv venv; \
		. venv/bin/activate && pip install -r requirements.txt; \
		echo "venv created and requirements installed."; \
	else \
		echo "venv already exists."; \
	fi

down:
	docker-compose down

destroy:
	rm -rf __pycache__ venv
	docker-compose down --rmi all --volumes --remove-orphans
	docker system prune -f
	@echo "Project destroyed, Docker images and volumes removed." 