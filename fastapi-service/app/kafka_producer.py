import json
import logging
import os
from confluent_kafka import Producer

logger = logging.getLogger("kafka-producer")

BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

producer = Producer({"bootstrap.servers": BOOTSTRAP_SERVERS})


def delivery_report(err, msg):
    if err is not None:
        logger.error("Delivery failed for %s: %s", msg.topic(), err)
    else:
        logger.debug(
            "Message delivered to %s [%d] at offset %d",
            msg.topic(),
            msg.partition(),
            msg.offset(),
        )


def send(topic: str, data: dict):
    payload = json.dumps(data).encode("utf-8")
    logger.debug("Producing to %s: %s", topic, data)
    producer.produce(topic, payload, callback=delivery_report)
    producer.flush()
