import asyncio
from abc import ABC, abstractclassmethod
from components.configs import DataSourceConfig, ViewConfig







class DataSource:

    option: str
    description: str

    def __init__(self, option:str, description:str):
        self.option = option
        self.description = description




class UsecaseListener(ABC):

    @abstractclassmethod
    def update(self, data, view_ctx, view_config: ViewConfig):
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

    async def _poll_data_and_update_listener(self, ctx, view_ctx, polling_function, config:DataSourceConfig, view_config: ViewConfig):
        placeholder = ctx.empty()
        update_counter_ctx = ctx.empty()
        stop = ctx.button("Stop Polling")
        update_counter = 0

        while self.initiate:

            if self.initiate and stop:
                self.initiate = False

            latest_data = polling_function(placeholder, config)

            if latest_data != self.current_data:
                update_counter += 1
                self.current_data = latest_data
                self.listener.update(self=self.listener, data=latest_data, view_ctx=view_ctx, view_config=view_config)
                update_counter_ctx.markdown(f"Updates Received : __{update_counter}__")

            await asyncio.sleep(config.polling_frequency)  
