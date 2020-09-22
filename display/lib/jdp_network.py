import urequests

from network import WLAN, STA_IF
from time import sleep_ms

# https://github.com/jczic/MicroWebCli

# C O N S T A N T S

# F U N C T I O N S

def wlan_connect(essid, password, timeout=15):
    wlan = WLAN(STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(essid,password)
        sleep_ms(100)
        for _ in range(timeout):
            if wlan.isconnected():
                break
            sleep_ms(1000)
    return wlan.isconnected()


def wlan_disconnect(timeout=15):
    wlan = WLAN(STA_IF)
    wlan.disconnect()
    if wlan.isconnected():
        sleep_ms(100)
        for _ in range(timeout):
            if not wlan.isconnected():
                break
            sleep_ms(1000)
    wlan.active(False)
    return not wlan.isconnected()

def get_json_from_url(url, essid, password, timeout=15):
    json_data = None
    try:
        if (wlan_connect(essid, password, timeout)):
            response = urequests.get(url)
            if (response.status_code == 200):
                json_data = response.json()
    finally:
        wlan_disconnect(timeout)
    return json_data

# E X C E P T I O N S

class WebException(Exception):
    pass

# E P A P E R  D E V I C E
class Web(object):

    def __init__(self):
	    pass