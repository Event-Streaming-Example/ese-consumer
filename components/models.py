import asyncio
from abc import ABC, abstractclassmethod

class DataSource:

    option: str
    description: str

    def __init__(self, option:str, description:str):
        self.option = option
        self.description = description


class BackendDSConfig:

    polling_endpoint: str
    frequency: int

    def __init__(self, protocol: str,  base_url: str, endpoint: str, frequecy: int) -> None:
        self.polling_endpoint = f"{protocol}://{base_url}{endpoint}"
        self.frequency = frequecy


class UsecaseListener(ABC):

    @abstractclassmethod
    def update(self, data, view_ctx):
        pass

    @abstractclassmethod
    def view(self, ctx):
        pass




class Usecase:

    option: str
    condition: str
    trigger: str
    action: str
    reason: str

    initiate: bool
    listener: UsecaseListener

    def __init__(self, option:str, condition:str, trigger:str, action: str, reason:str, listener:UsecaseListener):
        self.option = option
        self.condition = condition
        self.trigger = trigger
        self.action = action
        self.reason = reason
        self.initiate = False
        self.listener = listener
        self.current_data = {}
    
    def display(self, ctx):
        ctx.dataframe(data = {
            "Trigger" : self.trigger,
            "Condition" : self.condition,
            "Action" : self.action,
            "Reason" : self.reason
        }, use_container_width=True)

    def set_control(self, ctx, view_ctx, pannel):
        pannel(self, ctx, view_ctx)

    def results(self, ctx):
        self.listener.view(self=self.listener, ctx=ctx)

    async def _poll_backend(self, ctx, view_ctx, polling_function, config:BackendDSConfig):
        stop = ctx.button("Stop Polling")
        ctx.info(f"Polling BE@{config.polling_endpoint}")
        while self.initiate:
            if self.initiate and stop:
                self.initiate = False
            latest_data = polling_function(config)
            if latest_data != self.current_data:
                self.current_data = latest_data
                self.listener.update(self=self.listener, data=latest_data, view_ctx=view_ctx)
            await asyncio.sleep(config.frequency)

    async def _poll_kafka(self, ctx, view_ctx, polling_function, config):
        latest_data = polling_function(config)
        ctx.info(f"Polling Kafka is a work in progress | Dummy Data : {latest_data}")






class MailerConfig:

    queue_url: str
    channel: str

    def __init__(self, queue_url: str, channel: str) -> None:
        self.queue_url = queue_url
        self.channel = channel