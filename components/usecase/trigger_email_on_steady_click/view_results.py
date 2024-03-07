from typing import List
from datetime import datetime

from components.usecase.trigger_email_on_steady_click.models import EventMailTracker
from components.usecase.trigger_email_on_steady_click.constant import THRESHOLD_CONSECUTIVE_EVENTS, THRESHOLD_LIMIT_IN_EPOCH_MILLI, EMAIL_TO
from components.datasource import EventSubType
from components.usecase.trigger_email_on_steady_click.utility import format_timestamps, timestamp_delta_to_string




def view_sent_emails(view_ctx, data:List[EventMailTracker]): 
        result = []
        for item in data: 
            timestamps     = sorted([ts.timestamp for ts in item.logs])
            timestamps_str = format_timestamps(timestamps)
            duration       = timestamp_delta_to_string(abs(timestamps[-1] - timestamps[0]))
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
                   
        Below given IPs emmitted __{THRESHOLD_CONSECUTIVE_EVENTS}__ within a span of __{THRESHOLD_LIMIT_IN_EPOCH_MILLI/1000}__ seconds, an event of type `{EventSubType.KEY_PRESS_EVENT.value}`. An email was sent to {EMAIL_TO} for the downstream category to take any further action.
        """) 
        c.write("")
        c.dataframe(data=result, use_container_width=True)
