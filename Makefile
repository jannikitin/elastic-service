DOCKER_COMPOSE_LOCAL = docker-compose-local.yaml
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5000

MIGRATION_CMD = alembic upgrade heads

up:
	docker compose -f $(DOCKER_COMPOSE_LOCAL) up -d
migrate:
	DB_HOST=$(POSTGRES_HOST) DB_PORT=$(POSTGRES_PORT) DB_USER=$(POSTGRES_USER) DB_PASSWORD=$(POSTGRES_PASSWORD) DB_NAME=$(POSTGRES_DB) $(MIGRATION_CMD)
run-local: up migrate

down:
	docker compose -f $(DOCKER_COMPOSE_LOCAL) down && docker network prune --force && docker compose -f $(DOCKER_COMPOSE_LOCAL) rm --force
