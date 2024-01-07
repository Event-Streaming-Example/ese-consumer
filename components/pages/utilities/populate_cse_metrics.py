import datetime

CSE="CLICK_STREAM_EVENT"
KEY_PRESS_CSE="KEY_PRESS_EVENT"
BUTTON_CLICK_CSE="BUTTON_CLICK_EVENT"
INPUT_PASSED_CSE="INPUT_PASSED_EVENT"

def populate_cse_metrics(response, data_store):
    total_count = 0
    key_press_count = 0
    btn_press_count = 0
    inp_passed_count = 0
    for d in response:
        for event_log in d["eventLogs"]:
            if event_log["eventType"] == CSE:
                total_count += 1
            if event_log["data"]["event"] == KEY_PRESS_CSE:
                key_press_count += 1
            if event_log["data"]["event"] == BUTTON_CLICK_CSE:
                btn_press_count += 1
            if event_log["data"]["event"] == INPUT_PASSED_CSE:
                inp_passed_count += 1
    data_store.append({
        "Total" : total_count,
        "Key Press" : key_press_count,
        "Button Press" : btn_press_count,
        "Input Passed" : inp_passed_count,
        "timestamp" : datetime.datetime.now()
    })