# Startup Commands

This is a reference for docker startup commands.
Webserver for frontend, python flask running for backend, mongo running as database.
See relevant sections below.

## Network

docker network create --driver bridge thingnet

## Frontend

docker build --tag react .
docker run -dit --rm --network thingnet --name frontend -p 3000:3000 react

## Backend

docker build --tag flask .
docker run -dit --rm --network thingnet --name backend -p 5000:5000 --env-file .env flask

## Mongo

docker pull mongo
docker run -dit --rm --network thingnet --name db mongo

