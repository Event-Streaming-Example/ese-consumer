from components.datasource.kafka.models.configs import KafkaDSConfig


def fetch_latest_data(ctx, config: KafkaDSConfig):
    ctx.info(f"Polling Kafka is a work in progress using config : {config}")
    return "Kafka data"