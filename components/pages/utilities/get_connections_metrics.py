import datetime

from .populate_cse_metrics import CSE

def get_all_connections_event_count(data, data_store):
    for item in data:
        ip = item["ip"]
        cs_count = item["click_count"]
        ou_count = item["order_update_count"]
        if ip not in data_store:
            data_store[ip] = {
                "total_count" : cs_count + ou_count,
                "click_count" : cs_count,
                "order_count" : ou_count,
                "click_count_last5" : cs_count,
                "order_count_last5" : ou_count
            }
        else:
            if cs_count < data_store[ip]["click_count"]:
                data_store[ip]["click_count_last5"] = cs_count
            else:
                data_store[ip]["click_count"] = cs_count
                data_store[ip]["click_count_last5"] = cs_count
            if ou_count < data_store[ip]["order_count"]:
                data_store[ip]["order_count_last5"] = ou_count
            else:
                data_store[ip]["order_count"] = ou_count
                data_store[ip]["order_count_last5"] = ou_count
            data_store[ip]["total_count"] = data_store[ip]['click_count'] + data_store[ip]['order_count']
            

def get_all_connections(response, data_source):
    for ip_block in response:
        order_counts = 0
        click_counts = len([i for i in ip_block["eventLogs"] if i["eventType"] == CSE])
        data_source.append({
            "ip" : ip_block["ip"],
            "click_count" : click_counts,
            "order_update_count" : order_counts,
            "timestamp" : datetime.datetime.now()
        })

def display_connections(data_source):
    col_x_timestamp = []
    col_y_count = []
    col_z_ip = []
    for item in data_source:
        col_x_timestamp.append(item['timestamp'])
        col_y_count.append(item["click_count"] + item["order_update_count"])
        col_z_ip.append(item["ip"])
    return {
        "timestamp" : col_x_timestamp,
        "count" : col_y_count,
        "ip" : col_z_ip
    }