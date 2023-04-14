import socket
import json

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = None
        self.port = None
        self.addr = (self.server, self.port)
        self.client.settimeout(2)
    def connect(self):
        try:
            self.client.connect(self.addr)
            self.client.settimeout(None)
        except:
            pass
    def send(self, data):
        try:
            self.client.send(data)
            resp = self.client.recv(1024)
            print(resp)
            return json.loads(resp.decode('utf-8').split("}", 1)[0] + '}')
        except socket.error as e:
            print(e)
    def set_host(self, host):
        self.server = host
        self.addr = (self.server, self.port)
    def set_port(self, port):
        self.port = port
        self.addr = (self.server, self.port)
    def flush(self):
        try:
            self.client.close()
        except:
            pass
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(2)
