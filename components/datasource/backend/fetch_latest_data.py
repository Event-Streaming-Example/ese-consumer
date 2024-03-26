import requests
from typing import List, Dict
from components.datasource.backend.models.response import Event
from components.datasource.backend.models.configs import BackendDSConfig



def fetch_latest_data(ctx, config: BackendDSConfig) -> Dict[str, List[Event]]: 
    ctx.info(f"Polling BE@{config.polling_endpoint}")
    json_data = requests.get(config.polling_endpoint).json()
    return _deserialize_response(json_data)

def _deserialize_response(response): 
    result = {}
    for item in response: 
        events = []
        for event in item['event_logs']:
            events.append(Event(event))
        result[item['ip']] = events
    return result