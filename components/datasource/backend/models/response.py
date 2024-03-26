import time
from dataclasses import dataclass
from components.datasource import EventType, EventSubType



@dataclass
class Event: 

      type       : EventType
      sub_type   : EventSubType
      client_ts  : int
      server_ts  : int
      consumer_ts: int
      ip         : str
      data       : dict

      def __init__(self, json_data):
            self.type        = json_data['type']
            self.sub_type    = json_data['sub_type']
            self.client_ts   = json_data['client_ts']
            self.server_ts   = json_data['server_ts']
            self.consumer_ts = int(time.time() * 1000)
            self.ip          = json_data['ip']
            self.data        = json_data['data']

      def __eq__(self, __value: object) -> bool:
            return (self.client_ts == __value.client_ts) and (self.type == __value.type) and (self.sub_type == __value.sub_type)

      def get_producer_delta(self) -> int: 
            return self.server_ts - self.client_ts
      
      def get_consumer_delta(self) -> int: 
            return self.consumer_ts - self.server_ts