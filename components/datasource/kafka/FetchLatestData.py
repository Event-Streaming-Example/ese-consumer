from components.configs import KafkaDSConfig


def fetch(ctx, config: KafkaDSConfig):
    ctx.info(f"Polling Kafka is a work in progress using config : {config}")
    return "Kafka data"