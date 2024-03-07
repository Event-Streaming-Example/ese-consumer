from typing import List
from dataclasses import dataclass

from components.datasource.backend.models.interractor import Snapshot


@dataclass
class EventMailTracker():

    ip       : str
    logs     : List[Snapshot]
    sent_mail: bool