DOCKER_COMPOSE_LOCAL = docker-compose-local.yaml
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5000


up:
	docker compose -f $(DOCKER_COMPOSE_LOCAL) up -d
down:
	docker compose -f $(DOCKER_COMPOSE_LOCAL) down && docker network prune --force && docker compose -f $(DOCKER_COMPOSE_LOCAL) rm --force
