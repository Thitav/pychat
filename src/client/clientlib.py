from threading import Thread
import socket

class Client:
    def __init__(self):
        self.sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        with open('config.cfg', 'r') as file:
            config_data = file.readlines()
            file.close()

        ip = config_data[0].replace('\n', '').split('=')[1]
        port = int(config_data[1].replace('\n', '').split('=')[1])

        self.sck.connect((ip, port))

    def send(self, data):
        self.sck.send(data.encode())

    def recv(self):
        return self.sck.recv(1024).decode('utf-8')

class Receiver(Thread):
    def __init__(self, client):
        super(Receiver, self).__init__()
        self.client = client

    def run(self):
        while True:
            data = self.client.recv()
            print(data)