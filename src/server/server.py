import threading
import serverlib
import encrypt
import socket
import json
import sys
import os

users = {}

def cmd():
    while True:
        cmd = input('-> ')

        if cmd == 'exit':
            sck.close()
            os._exit(0)

def handler(conn):
    while True:
        new, username, password = conn.recv(1024).decode('utf-8').replace('\n', '').split(':')
        new = int(new)
        password = encrypt.sha256(password)

        json_data = json.load(open('storage.json', 'r'))

        if new:
            uid = str(len(json_data) + 1)

            json_data[uid] = {'username': username, 'password': password}
            json.dump(json_data, open('storage.json', 'w'))
            conn.send('auth'.encode())

            break
        else:
            auth = 0
            for i in json_data:
                if username == json_data[i]['username'] and password == json_data[i]['password']:
                    auth = i
                    break

            if auth:
                uid = auth
                conn.send('auth'.encode())
                break
            else:
                conn.send('error'.encode())

    user = serverlib.User(conn, uid, username)
    users[uid] = user
    while True:
        data = user.recv()

        for i in users:
            if not i == user.uid:
                users[i].send(data)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))

ip = s.getsockname()[0]
s.close()

port = int(sys.argv[1])

threading.Thread(target=cmd).start()

sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sck.bind((ip, port))
sck.listen(5)

while True:
    conn, addr = sck.accept()
    threading.Thread(target=handler, args=(conn,)).start()