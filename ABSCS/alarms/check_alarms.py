#This function takes in a telemetry JSON and checks all values for alarms. 
import json
from alarms.models import Alarms
from django.core.cache import cache
from channels.layers import get_channel_layer

def check_alarms(telem_packet:str|dict):
    mission_id = cache("mission_id")
    if type(telem_packet) is str:
        telem_packet = json.loads(telem)
    for telem in telem_packet("telem"):
        try:
            #TODO clean up the ifs in here
            alarm = Alarms.objects.get(mission_id=mission_id, mnemonic_name=telem("mnemonic"))
            telem_val = telem("value")
            if alarm.yellow_low < telem_val and telem_val < alarm.yellow_high:
                pass #No alarm!
            elif telem_val < alarm.yellow_low:
                if telem_val < alarm.red_low:
                    send_alarm_to_ws("red_low", telem("mnemonic"), alarm.red_low, telem_val, telem("timestamp"), alarm.message) 
                else:
                    send_alarm_to_ws("yellow_low", telem("mnemonic"), alarm.yellow_low, telem_val, telem("timestamp"), alarm.message) 
            elif telem_val < alarm.red_high:
                send_alarm_to_ws("yellow_high", telem("mnemonic"), alarm.yellow_high, telem_val, telem("timestamp"), alarm.message) 
            else:
                send_alarm_to_ws("red_high", telem("mnemonic"), alarm.red_high, telem_val, telem("timestamp"), alarm.message) 


        except Alarms.DoesNotExist:
            continue

def send_alarm_to_ws(severity:str,  mnemonic:str, alarm_lim:float, value:float,  timestamp:str, message:str):
    #Any code that needs to happen when an alarm is sent out can happen here
    #TODO: Implement logging! NEED to have long-term alarm logging
    channel_layer = get_channel_layer()
    channel_layer.group_send("alarm_group",
                                {"type": "send_alarm", "data" : {"severity" : severity, 
                                                                "mnemonic" : mnemonic, 
                                                                "alarm_lim" : alarm_lim,
                                                                "value" : value,
                                                                "timestamp" : timestamp,
                                                                "message" : message}
                                })