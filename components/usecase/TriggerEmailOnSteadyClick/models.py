import time

from dataclasses import dataclass
from typing import List

from components.datasource.backend.data_model import EventType, EventSubType


class Snapshot():

    timestamp: int
    server_timestamp: int
    event_type: EventType
    event_subtype: EventSubType

    def __init__(self, timestamp: int, server_timestamp: int, event_type: EventType, event_subtype: EventSubType):
        self.timestamp = timestamp
        self.server_timestamp = server_timestamp
        self.event_type = event_type
        self.event_subtype = event_subtype

    def get_producer_delta(self) -> int:
        return self.server_timestamp - self.timestamp
    
    def get_consumer_delta(self) -> int:
        return int(time.time() * 1000) - self.server_timestamp
    

@dataclass
class IPSnapshot():
    ip: str
    logs: List[Snapshot]