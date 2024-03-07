import time

from typing import List, Dict
from dataclasses import dataclass

from components.datasource import EventType, EventSubType



class Snapshot(): 

    timestamp       : int
    server_timestamp: int
    event_type      : EventType
    event_subtype   : EventSubType

    def __init__(self, timestamp: int, server_timestamp: int, event_type: EventType, event_subtype: EventSubType): 
        self.timestamp        = timestamp
        self.server_timestamp = server_timestamp
        self.event_type       = event_type
        self.event_subtype    = event_subtype

    def __eq__(self, __value: object) -> bool:
        return (self.timestamp == __value.timestamp) and (self.event_type == __value.event_type) and (self.event_subtype == __value.event_subtype)

    def get_producer_delta(self) -> int: 
        return self.server_timestamp - self.timestamp
    
    def get_consumer_delta(self) -> int: 
        return int(time.time() * 1000) - self.server_timestamp
    


class IpSnapshotLog():

    _snapshot_hash_map: Dict[str, List[Snapshot]]
    _snapshot_ip_list : List[str]

    @dataclass
    class _IpLogsEntity():
        ip: str
        logs: List[Snapshot]


    def __init__(self) -> None:
        self._snapshot_hash_map = {}
        self._snapshot_ip_list  = []


    def __sub__(self, other):
        result = IpSnapshotLog()
        for ip in self._snapshot_ip_list: 
            existing_logs = self._snapshot_hash_map[ip]
            overlapping_logs: List[Snapshot] = other.look_up(ip)
            remaining = [log for log in existing_logs if log not in overlapping_logs]
            if len(remaining) != 0:
                result.append(ip=ip, logs=remaining)
        return result


    def append(self, ip: str, logs:List[Snapshot]):
        if ip not in self._snapshot_ip_list: 
            self._snapshot_hash_map[ip] = sorted(logs, key=lambda x: x.timestamp)
            self._snapshot_ip_list.append(ip)
        else: 
            self._snapshot_hash_map[ip].extend(logs)
            self._snapshot_hash_map[ip] = sorted(self._snapshot_hash_map[ip], key=lambda x: x.timestamp)


    def look_up(self, ip: str) -> List[Snapshot]:
        if ip not in self._snapshot_ip_list: 
            return []
        return self._snapshot_hash_map[ip]
    

    def get_logs(self) -> List[Snapshot]:
        result: List[Snapshot] = []
        for ip in self._snapshot_ip_list: 
            result.extend(self._snapshot_hash_map[ip])
        return result
    

    def get_ips(self) -> List[str]:
        return self._snapshot_ip_list
    

    def filter_by_event_subtype(self, event_subtype: EventSubType):
        result = IpSnapshotLog()
        for key, value in self._snapshot_hash_map.items(): 
            filtered_list = [i for i in value if i.event_subtype == event_subtype]
            if len(filtered_list) != 0:
                result.append(ip=key, logs=filtered_list)
        return result
    

    def clear(self):
        self._snapshot_hash_map.clear()
        self._snapshot_ip_list.clear()

    def get_iterable(self) -> List[_IpLogsEntity]:
        result = []
        for key, value in self._snapshot_hash_map.items():
            result.append(self._IpLogsEntity(key, value))
        return result