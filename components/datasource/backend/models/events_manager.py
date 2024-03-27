from typing import List, Dict
from itertools import chain

from components.datasource import EventSubType
from components.datasource.backend.models.response import Event



class EventsManager():

    _event_logs: Dict[str, List[Event]]
    _marked_event_logs: Dict[str, List[Event]]

    def __init__(self) -> None:
        self._event_logs = {}
        self._marked_event_logs = {}

    def append(self, snapshot_data:Dict[str, List[Event]]):
        for ip, events in snapshot_data.items():
            if self._event_logs.get(ip):
                present_log = self._event_logs[ip]
                self._event_logs[ip].clear()
                self._event_logs[ip] = list(set(present_log + events))
            else:
                self._event_logs[ip] = events              
            self._event_logs[ip].sort(key=lambda x:x.client_ts)

    def get_all_events(self)->List[Event]:
        return list(chain.from_iterable([i for i in self._event_logs.values()]))
    
    def mark_event(self, ip:str, marked_event: Event):
        if self._marked_event_logs.get(ip):
            if marked_event not in self._marked_event_logs[ip]:
                self._marked_event_logs[ip].append(marked_event)
        else:
            self._marked_event_logs[ip] = [marked_event]

    def filter_unmarked(self, event_sub_type: EventSubType) -> Dict[str, List[Event]]:

        def _is_event_unmarked(ip: str, event: Event) -> bool:
            if self._marked_event_logs.get(ip) is None:
                return True
            return event not in self._marked_event_logs[ip]

        result: Dict[str, List[Event]] = {}
        for ip, events in self._event_logs.items():
            filtered_events: List[Event] = []
            for event in events:
                if (event.sub_type == event_sub_type.value) and (_is_event_unmarked(ip, event)):
                    filtered_events.append(event)
            if len(filtered_events) != 0:
                result[ip] = filtered_events
        return result
    
    def clear(self):
        self._event_logs.clear()
        self._marked_event_logs.clear()
