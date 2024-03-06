from components.abstractions import DataSourceConfig

class KafkaDSConfig(DataSourceConfig):

    frequency: int

    def __init__(self, frequency: int) -> None:
        super().__init__()
        self.frequency = frequency

    @property
    def polling_frequency(self):
        return self.frequency