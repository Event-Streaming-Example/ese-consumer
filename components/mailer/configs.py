from components.abstractions import ViewConfig



class MailerViewConfig(ViewConfig): 

    queue_url: str
    channel  : str

    def __init__(self, queue_url: str, channel: str) -> None: 
        super().__init__()
        self.queue_url = queue_url
        self.channel   = channel