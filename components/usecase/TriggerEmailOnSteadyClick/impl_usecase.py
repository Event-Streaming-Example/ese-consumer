from components.models import UsecaseListener
from components.configs import MailerViewConfig

BUCKET = []

class TriggerEmailOnSteadyClick(UsecaseListener):

    def __init__(self):
        super().__init__()

    def update(self, data, view_ctx, view_config: MailerViewConfig):
        BUCKET.append(data)
        live_data, log_data = view_ctx.columns(2)
        live_data.write(BUCKET)
        log_data.write(f"Pushing email to : {view_config.channel}@{view_config.queue_url}")

    def view(self, ctx):
        ctx.write(BUCKET)