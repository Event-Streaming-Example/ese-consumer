from typing import List
from datetime import datetime

from components.usecase.trigger_email_on_steady_click.models import EventMailTracker
from components.usecase.trigger_email_on_steady_click.constant import THRESHOLD_CONSECUTIVE_EVENTS, THRESHOLD_LIMIT_IN_EPOCH_MILLI, EMAIL_TO
from components.datasource import EventSubType
from components.usecase.trigger_email_on_steady_click.utility import format_timestamp, timestamp_delta_to_string




def view_sent_emails(view_ctx, data:List[EventMailTracker]): 
        result = []
        for item in data: 
            client_timestamp   = sorted([ts.client_ts for ts in item.logs])
            consumer_timestamp = sorted([ts.consumer_ts for ts in item.logs])

            activity_duration = timestamp_delta_to_string(abs(client_timestamp[-1] - client_timestamp[0]))
            detetction_lag    = timestamp_delta_to_string(abs(consumer_timestamp[-1] - client_timestamp[-1]))
            
            result.append({
                "IP Address"       : item.ip,
                "Activity Start"   : format_timestamp(client_timestamp[0]),
                "Activity End"     : format_timestamp(client_timestamp[-1]),
                "Activity Duration": activity_duration,
                "Detetction Lag"   : detetction_lag,
                "Email Sent"       : "✅" if item.sent_mail else "❌"
            })  
        c = view_ctx.container()
        c.markdown(f"""
        #### IPs with suspicious activity
                   
        Below given IPs emmitted __{THRESHOLD_CONSECUTIVE_EVENTS}__ within a span of __{THRESHOLD_LIMIT_IN_EPOCH_MILLI/1000}__ seconds, an event of type `{EventSubType.KEY_PRESS_EVENT.value}`. An email was sent to {EMAIL_TO} for the downstream category to take any further action.
        """) 
        c.write("")
        c.dataframe(data=result, use_container_width=True)
