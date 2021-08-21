import uuid

from confluent_kafka import KafkaError, Message  # type: ignore
from fastapi import APIRouter
from fastapi.logger import logger
from pydantic import BaseModel

from src.kafka_job import create_job

router = APIRouter()


class JobMessage(BaseModel):
    computation_type: str
    computation_value: str


@router.post("/message/send", tags=["message", "send", "kafka"])
async def send_message(job_message: JobMessage) -> dict:
    def message_sent_callback(err: KafkaError, msg: Message) -> None:
        if err is None:
            logger.info(
                f"Message sent to '{msg.topic()}' on Partition: '{msg.partition()}'  with offset: '{msg.offset()}'"
            )
            return
        logger.error(f"{err}")
        exit(1)

    unique_id = str(uuid.uuid4())
    create_job(
        dict(job_message),
        {"id": unique_id, "type": "computation"},
        unique_id,
        message_sent_callback,
    )
    return {}
