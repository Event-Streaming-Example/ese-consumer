from components.abstractions import DataSourceConfig
from components.datasource import EventSubType, EventType
from components.datasource.kafka.configs import KafkaDSConfig
from components.datasource.response import Event

from typing import List, Dict
from confluent_kafka import KafkaError, Consumer

import time
import json


KAFKA_MESSAGES = []

KAFKA_CONSUMER_MEMOIZED: Consumer
MEMOIZED_FLAG: bool = False

def fetch_latest_data(ctx, config: KafkaDSConfig) -> Dict[str, List[Event]]: 

    consumer = get_consumer(config)
    msg = consumer.poll(1.0)

    if msg is not None:
        message = consume_message(ctx, msg)
        if message is not None:
            KAFKA_MESSAGES.append(message)

    print(KAFKA_MESSAGES)


    ip = "some_ip"
    event_json = {
            "type" : EventType.CLICK_STREAM_EVENT,
            "sub_type" : EventSubType.KEY_PRESS_EVENT,
            "client_ts" : int(time.time() * 1000),
            "server_ts" : int(time.time() * 1000),
            "ip" : ip,
            "data" : {
                "some_key" : "some_value"
            }
        }
    events = []
    events.append(Event(event_json))
    return {
        ip : events
    }


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
        print(value)
        value['type'] = map_topic(msg.topic())
        value['client_ts'] = value['client_timestamp']
        value['server_ts'] = msg.timestamp()[1]
        return Event(value)