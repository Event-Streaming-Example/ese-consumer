from typing import List
from datetime import datetime

from components.usecase.trigger_email_on_steady_click.models import EventMailTracker
from components.usecase.trigger_email_on_steady_click.constant import THRESHOLD_CONSECUTIVE_EVENTS, THRESHOLD_LIMIT_IN_EPOCH_MILLI
from components.datasource import EventSubType


def _format_timestamps(timestamps: List[int]) ->List[str]: 
    return [datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] for ts in timestamps]


def _timestamp_delta_to_string(timestamp: int) -> str: 
    seconds      = timestamp         // 1000
    milliseconds = timestamp % 1000
    return f"{seconds}s {milliseconds}ms"


def view_sent_emails(view_ctx, data:List[EventMailTracker]): 
        result = []
        for item in data: 
            timestamps     = sorted([ts.timestamp for ts in item.logs])
            timestamps_str = _format_timestamps(timestamps)
            duration       = _timestamp_delta_to_string(abs(timestamps[-1] - timestamps[0]))
            result.append({
                "IP Address"    : item.ip,
                "Activity Start": timestamps_str[0],
                "Activity End"  : timestamps_str[-1],
                "Duration"      : duration,
                "Email Sent"    : "✅" if item.sent_mail else "❌"
            })  
        c = view_ctx.container()
        c.markdown(f"""
        #### IPs with suspicious activity
                   
        Below given IPs emmitted __{THRESHOLD_CONSECUTIVE_EVENTS}__ within a span of __{THRESHOLD_LIMIT_IN_EPOCH_MILLI/1000}__ seconds, an event of type `{EventSubType.KEY_PRESS_EVENT.value}`. An email was sent to click_updates@ese.org for the downstream category to take any further action.
        """) 
        c.write("")
        c.dataframe(data=result, use_container_width=True)
