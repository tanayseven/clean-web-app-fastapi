from configparser import ConfigParser
from os import environ
from pathlib import Path
from typing import Callable, Optional

from confluent_kafka import SerializingProducer, Message, KafkaError  # type: ignore
from confluent_kafka.schema_registry import SchemaRegistryClient  # type: ignore
from confluent_kafka.schema_registry.avro import AvroSerializer  # type: ignore
from confluent_kafka.serialization import StringSerializer  # type: ignore

environment = environ["APP_ENV"]
config = ConfigParser()
config.read(f"config-{environment}.ini")
bootstrap_servers = config.get("kafka-broker", "hostname")
schema_registry_hostname = config.get("kafka-schema-registry", "hostname")
job_topic_name = config.get("kafka-broker", "job-topic-name")
job_schema = config.get("kafka-schema-registry", "job-topic-schema")


def create_job(
    value: dict,
    headers: dict = None,
    key: str = None,
    callback: Optional[Callable[[KafkaError, Message], None]] = None,
) -> None:
    schema = (Path(".") / "src" / "kafka_schema" / job_schema).absolute().read_text()
    schema_registry_client = SchemaRegistryClient({"url": schema_registry_hostname})
    serializer = AvroSerializer(
        schema_registry_client, schema_str=schema, conf={"auto.register.schemas": True}
    )
    producer_conf = {
        "bootstrap.servers": bootstrap_servers,
        "value.serializer": serializer,
        "key.serializer": StringSerializer(),
    }
    producer = SerializingProducer(producer_conf)
    producer.produce(
        topic=job_topic_name,
        value=value,
        headers=headers,
        on_delivery=callback,
        key=key,
    )
    producer.flush()
