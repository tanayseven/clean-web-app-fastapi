from configparser import ConfigParser
from os import environ
from fastapi.logger import logger

environment = environ["APP_ENV"]
config: ConfigParser = ConfigParser()
config.read(f"config-{environment}.ini")
logger.debug(f"Read the config-{environment}.ini file")
