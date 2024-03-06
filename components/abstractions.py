from abc import ABC, abstractproperty, abstractclassmethod



class DataSourceConfig(ABC): 

    @abstractproperty
    def polling_frequency(self): pass


class ViewConfig(ABC): 

    def __init__(self) -> None: 
        super().__init__()


class UsecaseListener(ABC): 

    @abstractclassmethod
    def update(self, data, view_ctx, stats_ctx, view_config: ViewConfig): 
        pass

    @abstractclassmethod
    def view(self, view_ctx, stats_ctx): 
        pass