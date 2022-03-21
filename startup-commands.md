# Startup Commands

This is a reference for docker startup commands.
Webserver for frontend, python flask running for backend, mongo running as database.
See relevant sections below.

## Network

docker network create --driver bridge thingnet

## Frontend

docker build --tag react .
docker run -itp 3000:3000 --network thingnet --rm --name frontend react

## Backend

docker build --tag flask .
docker run -itp 5000:5000 --env-file .env --rm --network thingnet --name backend flask

## Mongo

docker run -it --network thingnet --rm --name db mongo:latest
