from components.abstractions import DataSourceConfig



class BackendDSConfig(DataSourceConfig): 

    polling_endpoint: str
    frequency       : int

    def __init__(self, protocol: str,  base_url: str, endpoint: str, frequecy: int) -> None: 
        super().__init__()
        self.polling_endpoint = f"{protocol}://{base_url}{endpoint}"
        self.frequency        = frequecy

    @property
    def polling_frequency(self): 
        return self.frequency