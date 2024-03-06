from typing import List

from components.abstractions import UsecaseListener
from components.mailer.configs import MailerViewConfig
from components.datasource.backend.models.response import EventIPSnapshotData
from components.datasource.backend.models.interractor import Snapshot, IPSnapshot
from components.datasource.backend.view_consumer_metrics import get_max_lag, view_lag_metrics


SNAPSHOT:List[IPSnapshot] = []


class TriggerEmailOnSteadyClick(UsecaseListener):


    def __init__(self):
        super().__init__()


    def update(self, data: List[EventIPSnapshotData], view_ctx, stats_ctx, view_config: MailerViewConfig):
        global SNAPSHOT
        SNAPSHOT = self._format_data(self, data)
        
        get_max_lag(SNAPSHOT)
        view_lag_metrics(stats_ctx)
        view_ctx.write(SNAPSHOT)


    def view(self, view_ctx, stats_ctx):
        global SNAPSHOT
        if view_ctx.button("Clear output"):
            SNAPSHOT.clear()
        view_ctx.write(SNAPSHOT)
        view_lag_metrics(stats_ctx)


    def _format_data(self, data: List[EventIPSnapshotData]) -> List[IPSnapshot]:
        result = []
        for item in data:
            logs = []
            for log in item.event_logs:
                logs.append(Snapshot(
                    timestamp=log.entity.timestamp,
                    server_timestamp=log.meta_data.server_timestamp,
                    event_type=log.entity.event_type,
                    event_subtype=log.entity.data.event
                ))
            result.append(IPSnapshot(item.ip, logs))
        return result
    