![yamdb_final](https://github.com/koxximus/foodgram-project/workflows/Foodgram/badge.svg)
# Foodgram 
# Working sample you can find 84.201.151.214


This project allows you to publish various recipes. Users can follow authors and add their recipes to favorite or shoping list.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You need to install Docker.

[install docker](https://docs.docker.com/engine/install/)

Install Docker Compose

[intall docker-compose](https://docs.docker.com/compose/install/)

### Installing

Go to directory with project and create .env file

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres # write your password
DB_HOST=db
DB_PORT=5432 
```

Build images with Docker-compose

```
$ sudo docker-compose create
```

## Deployment

Run services

```
$ sudo docker-compose up -d

```

Connect to web service with CONTAINER_ID

```
$ sudo docker exec -it CONTAINER_ID bash

```

Create superuser

```
root@CONTAINER_ID:/code# python manage.py createsuperuser

```

Load test data to database

```
root@CONTAINER_ID:/code# python manage.py loaddata fixtures.json

```

## Authors

* **Konstantin Knysh** - *Initial work* - [koxximus](https://github.com/koxximus)


