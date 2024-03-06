from components.datasource.kafka.models.configs import KafkaDSConfig



def get_kafka_ds_config(ctx) -> KafkaDSConfig: 
    ctx.info("This is a work in progress to get Kafka Config")
    return KafkaDSConfig(42)