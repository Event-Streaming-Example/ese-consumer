from typing import List

from components.mailer.configs import Mail
from components.usecase.trigger_email_on_steady_click.utility import format_timestamps, timestamp_delta_to_string
from components.datasource.backend.models.interractor import Snapshot
from components.datasource import EventSubType


THRESHOLD_LIMIT_IN_EPOCH_MILLI :int = 1000
THRESHOLD_CONSECUTIVE_EVENTS   :int = 3

EMAIL_FROM    = "consumer@ese.org"
EMAIL_TO      = "click_updated@ese.org"
EMAIL_SUBJECT = "[IP_ADDRESS] | Suspicious Activity Detected"
EMAIL_BODY    = f"{THRESHOLD_CONSECUTIVE_EVENTS} {EventSubType.KEY_PRESS_EVENT.value} events were generated from this IP from [START_TIME] to [END_TIME]. Total Duration of [DURATION]"

def build_email(ip: str, logs: List[Snapshot]) -> Mail: 
    ts        = sorted([t.timestamp for t in logs])
    ts_string = format_timestamps(ts)
    duration  = timestamp_delta_to_string(abs(ts[-1] - ts[0]))
    return Mail(
        _from    = EMAIL_FROM,
        _to      = EMAIL_TO,
        _subject = EMAIL_SUBJECT.replace("IP_ADDRESS", ip),
        _body    = EMAIL_BODY.replace("START_TIME", ts_string[0]).replace("END_TIME", ts_string[-1]).replace("DURATION", duration)
    )