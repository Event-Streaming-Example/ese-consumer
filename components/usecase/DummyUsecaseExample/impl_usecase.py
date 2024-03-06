from components.models import UsecaseListener
from components.configs import ViewConfig

class DummyUsecaseExample(UsecaseListener):

    def __init__(self) -> None:
        super().__init__()

    def update(self, data, view_ctx, stats_ctx, view_config: ViewConfig):
        view_ctx.write("Usecase received an update. Rebuilding view context")
        stats_ctx.write("Usecase received an update, Rebuilding stats context")

    def view(self, view_ctx, stats_ctx):
        view_ctx.write("Final data after polling")
        stats_ctx.write("Final consumer starts after polling")