import asyncio
from components.models import Usecase
from components.mailer.view_config_interractor import get_mailer_config
from components.datasource.kafka.view_config_interractor import get_kafka_ds_config
from components.datasource.backend.view_config_interractor import get_backend_ds_config
from components.datasource.backend.fetch_latest_data import fetch_latest_data as be_fetch_latest_data
from components.datasource.kafka.fetch_latest_data import fetch_latest_data as kafka_fetch_latest_data



def be_pannel(self: Usecase, ctx, view_ctx, stats_ctx): 

    be_config     = get_backend_ds_config(ctx)
    mailer_config = get_mailer_config(ctx)

    if mailer_config.channel != "" and mailer_config.queue_url != "": 
        if be_config.frequency != 0                                     : 
            if ctx.button("Initiate Polling")                               : 
                self.initiate = True
                asyncio.run(self._poll_data_and_update_listener(ctx, view_ctx, stats_ctx, be_fetch_latest_data, be_config, mailer_config))
        else: 
            ctx.error("Polling frequency should be greater than 1")
    else: 
        ctx.error("Provide Mailer Config to start polling")


def kafka_pannel(self: Usecase, ctx, view_ctx, stats_ctx): 
    kafka_config  = get_kafka_ds_config(ctx)
    mailer_config = get_mailer_config(ctx)
    asyncio.run(self._poll_data_and_update_listener(ctx, view_ctx, stats_ctx, kafka_fetch_latest_data, kafka_config, mailer_config))