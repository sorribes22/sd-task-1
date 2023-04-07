import os
import time

from src.implementation1.sensor.PollutionSensor import PollutionSensor
from src.implementation1.sensor.Sensor import Sensor
from src.implementation1.server.LoadBalancer import LoadBalancer
from src.implementation1.server.Server import Server
from src.implementation1.sensor.AirSensor import AirSensor

import threading
import sys


def start_all():
    print("Start all")
    threads = {
        threading.Thread(target=start_server, args=[20001]),
        threading.Thread(target=start_server, args=[20002]),
        threading.Thread(target=start_load_balancer),
        threading.Thread(target=start_sensor, args=[AirSensor]),
        threading.Thread(target=start_sensor, args=[PollutionSensor])
    }
    for t in threads:
        t.start()

    for t in threads:
        t.join()


def start_terminal():
    print("Start terminal")


def start_load_balancer():
    load_b = LoadBalancer()
    load_b.start_server()


def start_server(port: int):
    server = Server(port)
    server.start_server()


def start_sensor(s):
    time.sleep(1)
    sensor = s()


print("START")
if len(sys.argv) < 1:
    print("You have to provide parameters")
    sys.exit(1)
else:
    print("adeu")
arg1 = sys.argv[1]

switch = {
    "all": start_all,
    "terminal": start_terminal
}
func = switch.get(arg1, lambda: print("invalid case"))
func()
