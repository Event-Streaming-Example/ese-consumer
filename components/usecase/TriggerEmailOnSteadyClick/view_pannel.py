from components.datasource.backend.interractor import get_backend_ds_config
from components.datasource.kafka.interractor import get_kafka_ds_config

from components.datasource.backend.FetchLatestData import fetch as be_fetch
from components.datasource.kafka.FetchLatestData import fetch as kafka_fetch

from components.mailer.interractor import get_mailer_config
from components.models import Usecase

import asyncio


def be_pannel_teosc(self: Usecase, ctx, view_ctx, stats_ctx):
    be_config = get_backend_ds_config(ctx)
    mailer_config = get_mailer_config(ctx, be_config)


    if mailer_config.channel != "" and mailer_config.queue_url != "":
        if be_config.frequency != 0:
            if ctx.button("Initiate Polling"):
                self.initiate = True
                asyncio.run(self._poll_data_and_update_listener(ctx, view_ctx, stats_ctx, be_fetch, be_config, mailer_config))
        else:
            ctx.error("Polling frequency should be greater than 1")
    else:
        ctx.error("Provide Mailer Config to start polling")



def kafka_pannel_teosc(self: Usecase, ctx, view_ctx, stats_ctx):
    kafka_config = get_kafka_ds_config(ctx)
    mailer_config = get_mailer_config(ctx, kafka_config)
    asyncio.run(self._poll_data_and_update_listener(ctx, view_ctx, stats_ctx, kafka_fetch, kafka_config, mailer_config))