# Zillow Housing Forecast in AWS ECS (Elastic Container Service)

# How to run locally

## Prerequisites
Prerequisites to run: Python, Flask

## Instructions
1. Build the Dockerfile and name it
2. Modify docker-compose.yaml if you're starting with the official mariadb container
3. From a Git Bash command line:
* docker compose --build
* docker compose up -d

# Explaining the architecture and how it was set up

## Front end container 
The front end container is a Python Flask web app named "dstanecki/zhf". I built this using the Dockerfile present in this repo. It uses application.py to run the actual application on port 80. The connection to the database container contains hardcoded credentials and should be passed from AWS Secrets Manager or similar instead. 

## Back end container
The back end container is based on the official mariaDB container. I inserted data via an entrypoint script and committed those changes to my own container, "dstanecki/zhf_db". 

# ECS Task Definition 
Planning to replace the hardcoded credentials and need to figure out the best way to load data into ECS as an entrypoint script. 