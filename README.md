# fast-python-microservice


## Commands
```shell
poetry install # to install all the packages
./prun pytest --docker-compose=docker-compose.yaml --use-running-containers # run tests along with the docker containers
./prun pytest test/integration --docker-compose=docker-compose.yaml --use-running-containers # run only the integration tests
./prun pytest test/unit # run only the unit tests
./manage dev # run the server in dev mode

# Migration related
./prun alembic revision --autogenerate -m "<migration-name>" # generate a new migration
./prun alembic history # check the history of all the migrations
./prun alembic upgrade head  # apply all the migrations
./prun alembic downgrade <tag-name>  # rollback migrations
```
