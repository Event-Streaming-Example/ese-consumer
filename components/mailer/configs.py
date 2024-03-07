from dataclasses import dataclass

from components.abstractions import ViewConfig


@dataclass
class Mail: 

    _from   : str
    _to     : str
    _subject: str
    _body   : str

class MailerViewConfig(ViewConfig): 

    queue_url: str
    channel  : str

    def __init__(self, queue_url: str, channel: str) -> None: 
        super().__init__()
        self.queue_url = queue_url
        self.channel   = channel