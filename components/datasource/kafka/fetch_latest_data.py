from components.datasource import EventType
from components.datasource.kafka.configs import KafkaDSConfig
from components.datasource.response import Event

from typing import List, Dict
from confluent_kafka import KafkaError, Consumer

import json


KAFKA_EVENT_MESSAGE_MAP: Dict[str, List[Event]] = {}

KAFKA_CONSUMER_MEMOIZED: Consumer
MEMOIZED_FLAG: bool = False



def fetch_latest_data(ctx, config: KafkaDSConfig) -> Dict[str, List[Event]]: 

    global KAFKA_EVENT_MESSAGE_MAP
    consumer = get_consumer(config)
    msg = consumer.poll(1.0)

    if msg is not None:
        message = consume_message(ctx, msg)
        if message is not None:
            if KAFKA_EVENT_MESSAGE_MAP.get(message.ip):
                KAFKA_EVENT_MESSAGE_MAP[message.ip].append(message)
            else:
                KAFKA_EVENT_MESSAGE_MAP[message.ip] = [message]
        else: print("Message is None")
    else: print("Msg is None")


    return KAFKA_EVENT_MESSAGE_MAP



def get_consumer(config: KafkaDSConfig):
    global MEMOIZED_FLAG, KAFKA_CONSUMER_MEMOIZED
    if MEMOIZED_FLAG == False:
        consumer = config.kafka_consumer
        KAFKA_CONSUMER_MEMOIZED = consumer
        MEMOIZED_FLAG = True
        return consumer
    return KAFKA_CONSUMER_MEMOIZED



def map_topic(topic):
    if topic == 'click-events': return EventType.CLICK_STREAM_EVENT
    return EventType.ORDER_STATE_UPDATE_EVENT



def consume_message(ctx, msg):
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            ctx.error('%% %s [%d] reached end at offset %d\n' %
                  (msg.topic(), msg.partition(), msg.offset()))
        elif msg.error():
            ctx.error(msg.error())
        return None
    else:
        value = json.loads(msg.value().decode('utf-8'))
        value['type'] = map_topic(msg.topic())
        value['client_ts'] = value['client_timestamp']
        value['server_ts'] = msg.timestamp()[1]
        return Event(value)