#!/usr/bin/env python3

import RPi.GPIO as GPIO
import socketserver
import sys
import time

pins = {'on':27,'off':17}

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

socket_file = '/var/run/floathouse/listener.sock'

def execCmd(cmd):
    pin = pins[cmd]
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(pin,GPIO.LOW)

class FloathouseHandler(socketserver.BaseRequestHandler):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)

    def handle(self):
        self.data = self.request.recv(1024).strip()
        data = self.data.decode('utf-8').lower()
        try:
            execCmd(data)
            resp = data.upper()
        except KeyError:
            resp = "ERROR: unrecognized command '{}'".format(data)

        print("{} wrote '{}': \"{}\"".format(self.client_address[0], self.data, resp))
        self.request.sendall("{}\n".format(resp).encode('utf-8'))

class FloathouseServer(socketserver.TCPServer):
    allow_reuse_address = True

if __name__ == "__main__":
    #server = socketserver.UnixDatagramServer(socket_file, FloathouseHandler)
    HOST, PORT = '127.0.0.1', 8765
    server = FloathouseServer((HOST,PORT), FloathouseHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Exiting on ctrl-c")
    finally:
        server.server_close()

