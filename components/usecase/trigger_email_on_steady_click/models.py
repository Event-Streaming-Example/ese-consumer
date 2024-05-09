from typing import List
from dataclasses import dataclass
from components.datasource.response import Event


@dataclass
class EventMailTracker():

    ip       : str
    logs     : List[Event]
    sent_mail: bool
