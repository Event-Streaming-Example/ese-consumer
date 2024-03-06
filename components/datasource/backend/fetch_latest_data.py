import requests

from typing import List

from components.datasource.backend.models.response import EventIPSnapshotData, Entity, EventData, EventSubType, EventLog, EventType, MetaData
from components.datasource.backend.models.configs import BackendDSConfig

def fetch_latest_data(ctx, config: BackendDSConfig) -> List[EventIPSnapshotData]:
    ctx.info(f"Polling BE@{config.polling_endpoint}")
    json_data = requests.get(config.polling_endpoint).json()
    return _deserialize_response(json_data)

def _deserialize_response(response):
    result = []
    for item in response:
        event_logs = []
        for log_data in item['event_logs']:
            entity_data = log_data['entity']
            entity = Entity(
                event_type=EventType(entity_data['event_type']),
                timestamp=entity_data['timestamp'],
                ip=entity_data['ip'],
                data=EventData(event=EventSubType(entity_data['data']['event']))
            )
            meta_data = MetaData(server_timestamp=log_data['meta_data']['server_timestamp'])
            event_logs.append(EventLog(entity=entity, meta_data=meta_data))
        result.append(EventIPSnapshotData(ip=item['ip'], event_logs=event_logs))
    return result