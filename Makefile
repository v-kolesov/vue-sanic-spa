include .env
up:
	docker-compose up -d
upb:
	docker-compose up -d --force-recreate --build
stop:
	docker-compose stop
db:
	export PGPASSWORD=${POSTGRES_PASSWORD}; docker exec -it test_db psql -U $(POSTGRES_USER) ${POSTGRES_DB}
r:
	docker exec -it test_redis  /usr/local/bin/redis-cli
test:
	docker exec -it test_api pytest 
b:
	docker exec -it $(c) /bin/bash
