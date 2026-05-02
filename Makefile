run-server:
	uvicorn app.main:app --reload

# Local DB
up-local-db:
	docker compose -f docker-compose.postgres.local.yml up -d

down-local-db:
	docker compose -f docker-compose.postgres.local.yml down
