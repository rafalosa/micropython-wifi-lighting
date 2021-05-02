try:
    import usocket as socket
except:
    import socket

import network

import esp

esp.osdebug(None)

import gc

gc.collect()

file = open("credentials.txt","r")
file_content = file.readlines()
file.close()
ssid = file_content[0].replace("\n","")
password = file_content[1]

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass