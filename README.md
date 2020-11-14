# Foodgram

This project allows you to publish various recipes. Users can follow authors and add their recipes to favorite or shoping list.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You need to install Docker.

for Ubuntu:
1. Uninstall old versions

```
$ sudo apt-get remove docker docker-engine docker.io containerd runc
```
2. Set up the repository

```
$ sudo apt-get update

$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
```
3. Add Docker’s official GPG key

```
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```
4. Set up the stable repository

```
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```
5. Install Docker Engine:

```
$ sudo apt-get update
$ sudo apt-get install docker-ce docker-ce-cli containerd.io
```
[For other OS](https://docs.docker.com/engine/install/)

Install Docker Compose
For Ubuntu:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.27.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose
```
[For other OS](https://docs.docker.com/compose/install/)

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

Build images with Docker

```
$ sudo docker-compose create
```

## Deployment

Run services

```
$ sudo docker-compose start

```

Connect to web service with CONTAINER_ID

```
$ sudo docker exec -it CONTAINER_ID bash

```
Make migrations

```
root@CONTAINER_ID:/code# python manage.py migrate

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


