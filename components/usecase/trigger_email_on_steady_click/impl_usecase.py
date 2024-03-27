import streamlit as st
from typing import List, Dict
from components.abstractions import UsecaseListener
from components.mailer.configs import MailerViewConfig
from components.mailer.client import send_email
from components.datasource.backend.models.events_manager import EventsManager
from components.datasource.backend.models.response import EventSubType, Event
from components.datasource.backend.view_consumer_metrics import calculate_lag, view_lag_metrics
from components.usecase.trigger_email_on_steady_click.models import EventMailTracker
from components.usecase.trigger_email_on_steady_click.constant import THRESHOLD_CONSECUTIVE_EVENTS, THRESHOLD_LIMIT_IN_EPOCH_MILLI, build_email
from components.usecase.trigger_email_on_steady_click.view_results import view_sent_emails



EVENT_MAIL_TRACKER : List[EventMailTracker] = []
EVENTS_MANAGER     : EventsManager          = EventsManager()



class TriggerEmailOnSteadyClick(UsecaseListener): 


    def __init__(self): 
        super().__init__()


    def update(self, data: Dict[str, List[Event]], view_ctx, stats_ctx, view_config: MailerViewConfig): 
        global EVENTS_MANAGER
        EVENTS_MANAGER.append(data)

        calculate_lag(EVENTS_MANAGER.get_all_events())
        view_lag_metrics(stats_ctx)

        available_event_logs: Dict[str, List[Event]] = EVENTS_MANAGER.filter_unmarked(EventSubType.KEY_PRESS_EVENT)
        consecutive_event_logs: Dict[str, List[Event]] = self._filter_consecutive_event_logs(self, available_event_logs)
        self._flag_and_mark_events(self, consecutive_event_logs, view_config)

        view_sent_emails(view_ctx, EVENT_MAIL_TRACKER)



    def view(self, view_ctx, stats_ctx): 
        global EVENTS_MANAGER, EVENT_MAIL_TRACKER

        if view_ctx.button("Clear output"): 
            EVENTS_MANAGER.clear()
            EVENT_MAIL_TRACKER.clear()

        view_lag_metrics(stats_ctx)
        view_sent_emails(view_ctx, EVENT_MAIL_TRACKER)



    def _filter_consecutive_event_logs(self, events_logs:Dict[str, List[Event]]) -> Dict[str, List[Event]]:
        result: Dict[str, List[Event]] = {}
        for ip, events in events_logs.items():
            if len(events) > 1:
                consecutive_events: List[Event] = []
                consecutive_events.append(events[0])
                for i in range(1, len(events)):
                    if len(consecutive_events) != THRESHOLD_CONSECUTIVE_EVENTS:
                        if(abs(events[i].client_ts - events[i-1].client_ts) <= THRESHOLD_LIMIT_IN_EPOCH_MILLI):
                            consecutive_events.append(events[i])
                        else:
                            consecutive_events.clear()
                if len(consecutive_events) !=0:
                    result[ip] = consecutive_events
        return result


    def _flag_and_mark_events(self, event_log: Dict[str, List[Event]], config: MailerViewConfig):
        global EVENT_MAIL_TRACKER, EVENTS_MANAGER

        def _send_email(ip: str, logs: List[Event], config: MailerViewConfig) -> bool: 
            mail = build_email(ip, logs)
            try: 
                send_email(config, mail)
                return True
            except Exception as e: 
                st.error(f"There was an error sending email. [{e}]")
                return False

        for ip, consecutive_events in event_log.items():
            for event in consecutive_events:
                EVENTS_MANAGER.mark_event(ip, event)
            email_result = _send_email(ip, consecutive_events, config)
            EVENT_MAIL_TRACKER.append(EventMailTracker(
                ip        = ip,
                logs      = consecutive_events,
                sent_mail = email_result
            ))
