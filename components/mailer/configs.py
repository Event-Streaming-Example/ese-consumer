from dataclasses import dataclass

from components.abstractions import ViewConfig


@dataclass
class Mail: 

    _from   : str
    _to     : str
    _subject: str
    _body   : str

    def to_json(self): 
        return {
            "from"   : self._from,
            "to"     : self._to,
            "subject": self._subject,
            "content": self._body
        }

class MailerViewConfig(ViewConfig): 

    queue_url: str
    channel  : str

    def __init__(self, queue_url: str, channel: str) -> None: 
        super().__init__()
        self.queue_url = queue_url
        self.channel   = channel