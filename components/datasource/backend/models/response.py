from typing import List
from dataclasses import dataclass

from components.datasource import EventType, EventSubType



@dataclass
class EventData:
    event: EventSubType

@dataclass
class Entity:
    event_type: EventType
    timestamp: int
    ip: str
    data: EventData


@dataclass
class MetaData:
    server_timestamp: int


@dataclass
class EventLog:
    entity: Entity
    meta_data: MetaData

@dataclass
class EventIPSnapshotData:
    ip: str
    event_logs: List[EventLog]