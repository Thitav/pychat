class User:
    def __init__(self, conn, uid, username):
        self.conn = conn
        self.uid = uid
        self.username = username

    def send(self, data):
        self.conn.send(data.encode())

    def recv(self):
        data = self.conn.recv(1024).decode('utf-8')
        return data