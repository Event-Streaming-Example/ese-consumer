from components.abstractions import DataSourceConfig
from confluent_kafka import Consumer



class KafkaDSConfig(DataSourceConfig): 

    frequency: int
    topic    : str
    brokers  : str

    CONSUMER_GROUP_ID  = "ese.consumer.kafka_group_id"
    AUTO_OFFSET_RESET  = "earliest"
    ENABLE_AUTO_COMMIT = True

    def __init__(self, frequency: int, topic:str, brokers: str) -> None: 
        super().__init__()
        self.frequency = frequency
        self.topic     = topic
        self.brokers   = brokers

    @property
    def polling_frequency(self): 
        return self.frequency
    
    @property
    def kafka_consumer(self): 
        conf =  {
            'bootstrap.servers' : self.brokers,
            'group.id'          : self.CONSUMER_GROUP_ID,
            'auto.offset.reset' : self.AUTO_OFFSET_RESET,
            'enable.auto.commit': self.ENABLE_AUTO_COMMIT
        }
        consumer = Consumer(conf)
        consumer.subscribe([self.topic])
        return consumer