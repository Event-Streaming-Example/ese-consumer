from components.models import Usecase

def be_pannel_dummy(self: Usecase, ctx, view_ctx, stats_ctx):
    ctx.info("Populate this pannel to get the correct BE configuration for your usecase. Use the interractors from different modules to build the pannel")
    view_ctx.info("This is where the results of your usecase will be shown in real time")
    stats_ctx.info("Once the polling has started, this pannel will show the consumer and producer lag and other metrics")

def kafka_pannel_dummy(self: Usecase, ctx, view_ctx, stats_ctx):
    ctx.info("Populate this pannel to get the correct Kafka configuration for your usecase. Use the interractors from different modules to build the pannel")
    view_ctx.info("This is where the results of your usecase will be shown in real time")
    stats_ctx.info("Once the polling has started, this pannel will show the consumer and producer lag and other metrics")