# Zillow Housing Forecast 


# How to run locally

## Prerequisites
Prerequisites to run: Python, Flask

## Instructions
From a Git Bash command line:

docker compose --build
docker compose up -d

# Explaining the architecture and how it was set up

There is a frontend container and a backend container. The Dockerfile was used to build the zhf image. The mariaDB container was built off the stock mariaDB image and the init script was ran in the docker-compose-old.yaml file. Then while the containers were running, I saved it with "docker commit <containerID> zhf_db"