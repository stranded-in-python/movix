init:
	clone_and_fetch && docker compose -f local.yml --profiles init up -d


all:
	docker compose -f local.yml -f kafka.yml -f ugc-etl.local.yml --profiles all up -d

up:
	docker compose -f local.yml --profiles all up -d

admin:
	docker compose -f local.yml --profiles admin up -d

api:
	docker compose -f local.yml --profiles api up -d

auth:
	docker compose -f local.yml --profiles auth up -d

etl:
	docker compose -f local.yml --profiles etl up -d

notification:
	docker compose -f local.yml --profiles notification up -d

ugc:
	docker compose -f local.yml -f kafka.yml -f etl.local.yml --profiles ugc-api --profiles ugc-etl up -d

ugc-api:
	docker compose -f local.yml --profiles ugc-api up -d

ugc-etl:
	docker compose -f local.yml -f kafka.yml -f etl.local.yml --profiles ugc-etl up -d

ugc-api:
	docker compose -f local.yml --profiles ugc-api --profiles nginx --profiles logging up -d

down:
	docker-compose -f local.yml -f ugc-etl.local.yml -f kafka.yml --profiles all down

