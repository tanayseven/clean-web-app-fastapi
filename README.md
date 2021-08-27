# fast-python-microservice


## Commands
```shell
poetry install # to install all the packages
./prun pytest --use-running-containers # run tests along with the docker containers
./prun-test pytest test/integration --use-running-containers # run only the integration tests
./prun-test pytest test/integration --use-running-containers --pdb # run all tests to start pdb when it fails
./clean # cleans all the cache files that are created
./watch-test # run tests in watch mode
./manage dev # run the server in dev mode

# Migration related
./prun alembic revision --autogenerate -m "<migration-name>" # generate a new migration
./prun alembic history # check the history of all the migrations
./prun alembic upgrade head  # apply all the migrations
./prun alembic downgrade <tag-name>  # rollback migrations
```
