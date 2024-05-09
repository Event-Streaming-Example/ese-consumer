from components.datasource.kafka.configs import KafkaDSConfig



def get_kafka_ds_config(ctx) -> KafkaDSConfig: 
    ctx.markdown("##### Kafka Configuration")
    bkr_list_ctx, pol_feq_ctx = ctx.columns([1,1])

    polling_frequency = pol_feq_ctx.number_input("Polling frequency", value=5)
    broker_list = bkr_list_ctx.text_input("List of brokers", placeholder="broker1:19093, broker2:29093", value="192.168.29.191:19093, 192.168.29.191:29093")

    return KafkaDSConfig(polling_frequency, broker_list)