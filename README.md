# Movix

[![API](https://github.com/stranded-in-python/movix-api/actions/workflows/ci.yml/badge.svg)](https://github.com/stranded-in-python/movix-api/actions/workflows/ci.yml)
[![ETL](https://github.com/stranded-in-python/movix-etl/actions/workflows/ci.yml/badge.svg)](https://github.com/stranded-in-python/movix-etl/actions/workflows/ci.yml)
[![Admin](https://github.com/stranded-in-python/movix-admin/actions/workflows/ci.yml/badge.svg)](https://github.com/stranded-in-python/movix-admin/actions/workflows/ci.yml)

## What is this?

This is a project of 7th group of 24th stream of Yandex Practicum for Middle Python Developers. The goal of the project is to build a online streaming platform.

## What is under the hood?

Django 4.1, Elasticsearch, Redis, Postgres, FastAPI

## How to install

You need to make shure, that ElasticSearch is configured properly on your machine to run this project: [StackOverflow Link](https://stackoverflow.com/questions/51445846/elasticsearch-max-virtual-memory-areas-vm-max-map-count-65530-is-too-low-inc)

For local installation run:

```bash
git clone git@github.com:stranded-in-python/movix.git && cd movix && clone_and_fetch
docker compose -f local.yml up -d
```

## Deployment

For deployment you could use [Docker Swarm](https://docs.docker.com/engine/swarm/).

Configure Swarm, as described in [manual](https://dockerswarm.rocks/).

Then you need to create .env files for production at `.envs/.production`.
An example what .env files should look like lies at `.envs/.production.example/*`.

Then run:

```
export COMPOSE_PROJECT_NAME=movix_production
docker stack deploy -c production.yml
```
