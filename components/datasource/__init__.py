from enum import Enum



class EventType(Enum): 
    CLICK_STREAM_EVENT       = "CLICK_STREAM_EVENT"
    ORDER_STATE_UPDATE_EVENT = "ORDER_STATE_UPDATE_EVENT"


class EventSubType(Enum): 
    KEY_PRESS_EVENT    = "KEY_PRESS_EVENT"
    BUTTON_CLICK_EVENT = "BUTTON_CLICK_EVENT"
    INPUT_PASSED_EVENT = "INPUT_PASSED_EVENT"

    ORDER_CREATED   = "ORDER_CREATED"
    ORDER_ALLOCATED = "ORDER_ALLOCATED"
    ORDER_STARTED   = "ORDER_STARTED"
    ORDER_COMPLETED = "ORDER_COMPLETED"