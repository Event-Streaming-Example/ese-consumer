from components.models import UsecaseListener
from components.configs import ViewConfig

class DummyUsecaseExample(UsecaseListener):

    def __init__(self) -> None:
        super().__init__()

    def update(self, data, view_ctx, view_config: ViewConfig):
        view_ctx.write("Usecase received an update after polling")

    def view(self, ctx):
        ctx.write("Final data after polling")