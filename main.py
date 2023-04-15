#!/bin/bash
import time

from src.Configuration import Configuration
from src.implementation1.proxy.Proxy import Proxy as gRPC_Proxy
from src.implementation1.sensor.PollutionSensor import PollutionSensor as gRPC_PollutionSensor
from src.implementation1.server.LoadBalancer import LoadBalancer as gRPC_LoadBalancer
from src.implementation1.server.Server import Server as gRPC_Server
from src.implementation1.sensor.AirSensor import AirSensor as gRPC_AirSensor
from src.implementation2.server.Server import Server as rabbitmq_Server
from src.implementation2.sensor.AirSensor import AirSensor as rabbitmq_AirSensor
from src.implementation2.sensor.PollutionSensor import PollutionSensor as rabbitmq_PollutionSensor
from src.implementation2.terminal.Terminal import Terminal as rabbitmq_Terminal
from src.implementation2.proxy.Proxy import Proxy as rabbitmq_Proxy

import threading
import sys

from src.implementation1.terminal.Terminal import Terminal


def start_grpc_infraestructure():
    print("Starting gRPC infraestructure...")
    threads = {
        threading.Thread(target=start_grpc_server, args=[20001]),
        threading.Thread(target=start_grpc_server, args=[20002]),
        threading.Thread(target=start_grpc_load_balancer),
        threading.Thread(target=start_sensor, args=[gRPC_AirSensor]),
        threading.Thread(target=start_sensor, args=[gRPC_PollutionSensor]),
        threading.Thread(target=start_grpc_proxy)
    }
    for t in threads:
        t.start()

    for t in threads:
        t.join()


def start_rabbitmq_infraestructure():
    print("Starting RabbitMQ infraestructure...")
    threads = {
        threading.Thread(target=start_rabbitmq_server),
        threading.Thread(target=start_rabbitmq_server),
        threading.Thread(target=start_sensor, args=[rabbitmq_AirSensor]),
        threading.Thread(target=start_sensor, args=[rabbitmq_PollutionSensor]),
        threading.Thread(target=start_rabbitmq_proxy)
    }
    for t in threads:
        t.start()

    for t in threads:
        t.join()


def start_grpc_terminal():
    terminal_index = int(sys.argv[2])

    terminal_url = Configuration.get('terminal_urls')[terminal_index]
    terminal = Terminal(terminal_url['port'])
    terminal.start()


def start_grpc_load_balancer():
    load_b = gRPC_LoadBalancer()
    load_b.start_server()


def start_grpc_server(port: int):
    server = gRPC_Server(port)
    server.start_server()

def start_rabbitmq_server():
    server = rabbitmq_Server()
    server.start_server()

def start_rabbitmq_proxy():
    time.sleep(2)
    proxy = rabbitmq_Proxy()
    proxy.start()


def start_rabbitmq_terminal():
    terminal = rabbitmq_Terminal()
    terminal.start()



def start_sensor(s):
    time.sleep(1)
    sensor = s()


def start_grpc_proxy():
    time.sleep(2)
    proxy = gRPC_Proxy()
    proxy.start()


print("START")
if len(sys.argv) < 1:
    print("You have to provide parameters")
    sys.exit(1)

arg1 = sys.argv[1]

switch = {
    "grpc": start_grpc_infraestructure,
    "grpc_terminal": start_grpc_terminal,
    "rabbitmq": start_rabbitmq_infraestructure,
    "rabbitmq_terminal": start_rabbitmq_terminal

}
func = switch.get(arg1, lambda: print("invalid case"))
func()
