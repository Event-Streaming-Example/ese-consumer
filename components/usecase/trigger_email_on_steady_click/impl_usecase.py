import streamlit as st

from typing import List

from components.abstractions import UsecaseListener
from components.mailer.configs import MailerViewConfig
from components.datasource.backend.models.response import EventIPSnapshotData, EventSubType
from components.datasource.backend.models.interractor import Snapshot, IpSnapshotLog
from components.datasource.backend.view_consumer_metrics import get_max_lag, view_lag_metrics
from components.usecase.trigger_email_on_steady_click.models import EventMailTracker


SNAPSHOT_LOG: IpSnapshotLog

MARKED_SNAPSHOT_LOG = IpSnapshotLog()
EVENT_MAIL_TRACKER: List[EventMailTracker] = []


THRESHOLD_LIMIT_IN_EPOCH_MILLI :int = 1000
THRESHOLD_CONSECUTIVE_EVENTS   :int = 3


class TriggerEmailOnSteadyClick(UsecaseListener): 

    def __init__(self): 
        super().__init__()

    def update(self, data: List[EventIPSnapshotData], view_ctx, stats_ctx, view_config: MailerViewConfig): 
        self._format_data(self, data)
        
        get_max_lag(SNAPSHOT_LOG)
        view_lag_metrics(stats_ctx)

        self._find_and_send_mail(self)
        self._view_sent_emails(self, view_ctx)

    def view(self, view_ctx, stats_ctx): 
        global SNAPSHOT_LOG
        if view_ctx.button("Clear output"): 
            SNAPSHOT_LOG.clear()
        self._view_sent_emails(self, view_ctx)
        view_lag_metrics(stats_ctx)

    def _format_data(self, data: List[EventIPSnapshotData]): 
        global SNAPSHOT_LOG
        updated_data = IpSnapshotLog()
        for item in data: 
            logs:List[Snapshot] = []
            for log in item.event_logs: 
                logs.append(Snapshot(
                    timestamp        = log.entity.timestamp,
                    server_timestamp = log.meta_data.server_timestamp,
                    event_type       = log.entity.event_type,
                    event_subtype    = log.entity.data.event
                ))
            updated_data.append(ip=item.ip, logs=logs)
        SNAPSHOT_LOG = updated_data
    


    def _filter_snapshots(self, response: IpSnapshotLog, marked: IpSnapshotLog) -> IpSnapshotLog:
        available = response - marked
        return available.filter_by_event_subtype(EventSubType.KEY_PRESS_EVENT)



    def _get_consecutive_click_snapshots(self, data:List[Snapshot]) -> List[Snapshot]: 
        consecutive_snapshots: list[Snapshot] = []
        if(len(data) < THRESHOLD_CONSECUTIVE_EVENTS ): return consecutive_snapshots
        consecutive_snapshots.append(data[0])

        for i in range(1, len(data))                                  : 
            if len(consecutive_snapshots) == THRESHOLD_CONSECUTIVE_EVENTS: 
                return consecutive_snapshots
            if(abs(data[i].timestamp - data[i-1].timestamp) <= THRESHOLD_LIMIT_IN_EPOCH_MILLI): 
                consecutive_snapshots.pop()
                consecutive_snapshots.append(data[i-1])
                consecutive_snapshots.append(data[i])
            else: 
                consecutive_snapshots.clear()
        return consecutive_snapshots
    
    def _find_and_send_mail(self): 
        global SNAPSHOT_LOG, MARKED_SNAPSHOT_LOG, EVENT_MAIL_TRACKER
        filtered_snapshot: IpSnapshotLog = self._filter_snapshots(self, SNAPSHOT_LOG, MARKED_SNAPSHOT_LOG)


        for snapshot in filtered_snapshot.get_iterable():
            consecutive_logs = self._get_consecutive_click_snapshots(self, snapshot.logs)
            if len(consecutive_logs) != 0:
                EVENT_MAIL_TRACKER.append(EventMailTracker(
                    ip=snapshot.ip,
                    logs=consecutive_logs,
                    sent_mail=True
                ))
                MARKED_SNAPSHOT_LOG.append(snapshot.ip, consecutive_logs)


    def _view_sent_emails(self, view_ctx):
        result = []
        for item in EVENT_MAIL_TRACKER:
            result.append({
                "ip" : item.ip,
                "instances" : [ts.timestamp for ts in item.logs],
                "mail sent" : item.sent_mail
            })     
        view_ctx.json(result)
