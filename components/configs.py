from abc import ABC, abstractproperty



class DataSourceConfig(ABC):
    @abstractproperty
    def polling_frequency(self): pass




class BackendDSConfig(DataSourceConfig):

    polling_endpoint: str
    frequency: int

    def __init__(self, protocol: str,  base_url: str, endpoint: str, frequecy: int) -> None:
        super().__init__()
        self.polling_endpoint = f"{protocol}://{base_url}{endpoint}"
        self.frequency = frequecy

    @property
    def polling_frequency(self):
        return self.frequency




class KafkaDSConfig(DataSourceConfig):

    frequency: int

    def __init__(self, frequency: int) -> None:
        super().__init__()
        self.frequency = frequency

    @property
    def polling_frequency(self):
        return self.frequency





class ViewConfig(ABC):
    def __init__(self) -> None:
        super().__init__()




class MailerViewConfig(ViewConfig):

    queue_url: str
    channel: str
    data_source: DataSourceConfig

    def __init__(self, queue_url: str, channel: str, config: DataSourceConfig) -> None:
        super().__init__()
        self.queue_url = queue_url
        self.channel = channel
        self.data_source = DataSourceConfig