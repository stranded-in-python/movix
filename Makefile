init:
	./get_projects && docker compose -f local.yml --profile init up -d


all:
	docker compose -f local.yml -f kafka.yml -f ugc-etl.local.yml --profile all up -d

up:
	docker compose -f local.yml --profile all up -d

admin:
	docker compose -f local.yml --profile admin up -d

api:
	docker compose -f local.yml --profile api up -d

auth:
	docker compose -f local.yml --profile auth up -d

etl:
	docker compose -f local.yml --profile etl up -d

notification:
	docker compose -f local.yml --profile notification up -d

ugc:
	docker compose -f local.yml -f kafka.yml -f etl.local.yml --profile ugc-api --profile ugc-etl up -d

ugc-api:
	docker compose -f local.yml --profile ugc-api up -d

ugc-etl:
	docker compose -f local.yml -f kafka.yml -f etl.local.yml --profile ugc-etl up -d

ugc-api:
	docker compose -f local.yml --profile ugc-api --profile nginx --profile logging up -d

billing:
	docker compose -f local.yml --profile billing up -d --build

down:
	docker-compose -f local.yml -f ugc-etl.local.yml -f kafka.yml --profile all down
