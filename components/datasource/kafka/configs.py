from components.abstractions import DataSourceConfig



class KafkaDSConfig(DataSourceConfig): 

    frequency: int
    brokers: str

    def __init__(self, frequency: int, brokers: str) -> None: 
        super().__init__()
        self.frequency = frequency
        self.brokers = brokers

    @property
    def polling_frequency(self): 
        return self.frequency
    
    @property
    def broker_list(self):
        return self.brokers.replace(" ","").split(",")