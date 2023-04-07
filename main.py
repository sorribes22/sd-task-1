#!/bin/bash
import os
import time

from src.Configuration import Configuration
from src.implementation1.proxy.Proxy import Proxy
from src.implementation1.sensor.PollutionSensor import PollutionSensor
from src.implementation1.sensor.Sensor import Sensor
from src.implementation1.server.LoadBalancer import LoadBalancer
from src.implementation1.server.Server import Server
from src.implementation1.sensor.AirSensor import AirSensor

import threading
import sys

from src.implementation1.terminal.Terminal import Terminal


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
    terminal_index = int(sys.argv[2])

    terminal_url = Configuration.get('terminal_urls')[terminal_index]
    terminal = Terminal(terminal_url['port'])
    terminal.start()


def start_load_balancer():
    load_b = LoadBalancer()
    load_b.start_server()


def start_server(port: int):
    server = Server(port)
    server.start_server()


def start_sensor(s):
    time.sleep(1)
    sensor = s()


def start_proxy():
    time.sleep(2)
    proxy = Proxy()
    proxy.start()

print("START")
if len(sys.argv) < 1:
    print("You have to provide parameters")
    sys.exit(1)

arg1 = sys.argv[1]

switch = {
    "all": start_all,
    "terminal": start_terminal
}
func = switch.get(arg1, lambda: print("invalid case"))
func()
