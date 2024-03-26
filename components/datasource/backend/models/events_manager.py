from typing import List, Dict
from itertools import chain

from components.datasource import EventSubType
from components.datasource.backend.models.response import Event


class EventTracker():

    _event: Event
    _is_marked: bool

    def __init__(self, event) -> None:
        self._event = event
        self._is_marked = False

    def to_event(self) -> Event:
        return self._event





def to_event_tracker_list(events: List[Event]) -> List[EventTracker]:
    return [EventTracker(i) for i in events]

def from_event_tracker_list(event_trackers: List[EventTracker]) -> List[Event]:
    return [i.to_event() for i in event_trackers]

def get_item_index(event_trackers: List[EventTracker], target:Event) -> int:
    for index, obj in enumerate(event_trackers):
        if obj.to_event() == target:
            return index
    return -1





class EventsManager():

    _event_ip_logs       : Dict[str, List[EventTracker]]
    _ip_list             : List[str]

    def __init__(self) -> None:
        self._event_ip_logs        = {}
        self._ip_list              = []

    def append(self, snapshot_data:Dict[str, List[Event]]):
        for ip, events in snapshot_data.items():
            event_trackers = to_event_tracker_list(events)
            if ip in self._ip_list:
                if len(events) > len(self._event_ip_logs[ip]):
                    self._event_ip_logs[ip].extend(event_trackers)
                else:
                    return
            else:
                self._event_ip_logs[ip] = event_trackers
                self._ip_list.append(ip)
            self._event_ip_logs[ip].sort(key=lambda x:x._event.client_ts)

    def get_all_events(self)->List[Event]:
        return [event_trackers.to_event() for event_trackers in list(chain.from_iterable([i for i in self._event_ip_logs.values()]))]
    
    def mark_event(self, ip_addr:str, event: Event):
        for ip, event_trackers in self._event_ip_logs.items():
            if ip == ip_addr:
                index = get_item_index(event_trackers, event)
                if index != -1:
                    self._event_ip_logs[ip_addr][index]._is_marked = True
                    return

    def filter_unmarked(self, event_sub_type: EventSubType) -> Dict[str, List[Event]]:
        result: Dict[str, List[Event]] = {}
        for ip, events in self._event_ip_logs.items(): 

            filtered_events:List[Event] = []
            for event in events:
                if (not event._is_marked) and (event._event.sub_type == event_sub_type.value):
                    filtered_events.append(event.to_event())
            if len(filtered_events) != 0:
                result[ip] = filtered_events
        print([len(i) for i in result.values()])
        return result
    
    def clear(self):
        self._event_ip_logs.clear()
        self._ip_list.clear()

    def debug(self):
        for ip, event in self._event_ip_logs.items():
            print(f"{ip} : [{[(i._event.client_ts, i._is_marked) for i in event]}]")