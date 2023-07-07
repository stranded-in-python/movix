init:
	clone_and_fetch

upfull:
	docker compose -f local.yml -f kafka.yml up -d

up:
	
	docker compose -f local.yml up -d

down:
	docker-compose -f local.yml -f kafka.yml down

