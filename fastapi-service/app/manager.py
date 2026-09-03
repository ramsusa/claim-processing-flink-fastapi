from .kafka_producer import send


def publish_manager_action(action: dict):
    """
    Publish manager decision (RELEASE/REJECT) to Kafka.
    """
    send("claim.release", action)
    return action
