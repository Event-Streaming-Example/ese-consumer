from components.datasource import EventSubType, EventType
from components.datasource.kafka.configs import KafkaDSConfig
from components.datasource.response import Event

from typing import List, Dict
import time




def fetch_latest_data(ctx, config: KafkaDSConfig) -> Dict[str, List[Event]]: 
    ctx.info(f"Polling Kafka is a work in progress using config : {config}")
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