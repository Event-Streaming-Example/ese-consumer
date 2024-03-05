from components.models import Usecase

def be_pannel_dummy(self: Usecase, ctx, view_ctx):
    ctx.info("Populate this pannel to get the correct BE configuration for your usecase. Use the interractors from different modules to build the pannel")
    view_ctx.info("Pass this context to the _poll_data_and_update_listener method of the usecase")

def kafka_pannel_dummy(self: Usecase, ctx, view_ctx):
    ctx.info("Populate this pannel to get the correct Kafka configuration for your usecase. Use the interractors from different modules to build the pannel")
    view_ctx.info("Pass this context to the _poll_data_and_update_listener method of the usecase")