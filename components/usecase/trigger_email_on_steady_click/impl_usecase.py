import streamlit as st

from typing import List

from components.abstractions import UsecaseListener
from components.mailer.configs import MailerViewConfig, Mail
from components.mailer.client import send_email
from components.datasource.backend.models.response import EventIPSnapshotData, EventSubType
from components.datasource.backend.models.interractor import Snapshot, IpSnapshotLog
from components.datasource.backend.view_consumer_metrics import get_max_lag, view_lag_metrics
from components.usecase.trigger_email_on_steady_click.models import EventMailTracker
from components.usecase.trigger_email_on_steady_click.constant import THRESHOLD_CONSECUTIVE_EVENTS, THRESHOLD_LIMIT_IN_EPOCH_MILLI, build_email
from components.usecase.trigger_email_on_steady_click.view_results import view_sent_emails


# This will be overwritten on each call. Hence not initializing
SNAPSHOT_LOG       : IpSnapshotLog

# This will be created just once and then appended to
MARKED_SNAPSHOT_LOG: IpSnapshotLog = IpSnapshotLog()
EVENT_MAIL_TRACKER : List[EventMailTracker] = []


class TriggerEmailOnSteadyClick(UsecaseListener): 


    def __init__(self): 
        super().__init__()


    def update(self, data: List[EventIPSnapshotData], view_ctx, stats_ctx, view_config: MailerViewConfig): 
        self._format_data(self, data)
        
        get_max_lag(SNAPSHOT_LOG)
        view_lag_metrics(stats_ctx)

        self._find_and_send_mail(self, view_config)
        view_sent_emails(view_ctx, EVENT_MAIL_TRACKER)


    def view(self, view_ctx, stats_ctx): 
        global SNAPSHOT_LOG

        if view_ctx.button("Clear output"): 
            SNAPSHOT_LOG.clear()

        view_lag_metrics(stats_ctx)
        view_sent_emails(view_ctx, EVENT_MAIL_TRACKER)


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
        consecutive_snapshots                                                        : list[Snapshot] = []

        if (len(data) < THRESHOLD_CONSECUTIVE_EVENTS ):
            return consecutive_snapshots
        
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
    

    def _send_email(self, ip: str, logs: List[Snapshot], config: MailerViewConfig) -> bool: 
        mail = build_email(ip, logs)
        try: 
            send_email(config, mail)
            return True
        except Exception as e: 
            st.error(f"There was an error sending email. [{e}]")
            return False


    def _find_and_send_mail(self, config: MailerViewConfig): 
        global SNAPSHOT_LOG, MARKED_SNAPSHOT_LOG, EVENT_MAIL_TRACKER
        filtered_snapshot: IpSnapshotLog = self._filter_snapshots(self, SNAPSHOT_LOG, MARKED_SNAPSHOT_LOG)

        for snapshot in filtered_snapshot.get_iterable(): 
            consecutive_logs = self._get_consecutive_click_snapshots(self, snapshot.logs)
            if len(consecutive_logs) != 0:
                email_result = self._send_email(self, snapshot.ip, consecutive_logs, config)
                EVENT_MAIL_TRACKER.append(EventMailTracker(
                    ip        = snapshot.ip,
                    logs      = consecutive_logs,
                    sent_mail = email_result
                ))
                MARKED_SNAPSHOT_LOG.append(snapshot.ip, consecutive_logs)
