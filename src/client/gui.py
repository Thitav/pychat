import PySimpleGUI as sg
import clientlib as client
import os

class Error:
    def __init__(self, message):
        layout = [
            [sg.Text(message)],
            [sg.Button('Close')] 
        ]

        self.window = sg.Window('Error').layout(layout)

    def start(self):
        while True: 
            self.event, self.values = self.window.Read()

            if self.event in (sg.WIN_CLOSED, 'Close'):
                break

        self.close()

    def close(self):
        self.window.close()

class Login:
    def __init__(self):
        global username
        global user
        user = client.Client()

        layout = [
            [sg.Text('Username:'), sg.Input()],
            [sg.Text('Password:'), sg.Input()],
            [sg.Button('Login'), sg.Button('Register')] 
        ]

        self.window = sg.Window('Login').layout(layout)

    def start(self):
        global username

        while True:
            self.event, self.values = self.window.Read()

            if self.event in (sg.WIN_CLOSED, 'EXIT'):
                break

            if self.event == 'Login':
                user.send(f'0:{self.values[0]}:{self.values[1]}')
                res = user.recv()

                if res == 'error':
                    error = Error('Error logging in')
                    error.start()
                else:
                    username = self.values[0]
                    break

            if self.event == 'Register':
                user.send(f'1:{self.values[0]}:{self.values[1]}')
                res = user.recv()

                if res == 'error':
                    error = Error('Error registering user')
                    error.start()
                else:
                    username = self.values[0]
                    break

        self.close()

    def close(self):
        self.window.close()

class Chat:
    def __init__(self):
        layout = [
            [sg.Text('Chat:', size=(40, 1))],
            [sg.Output(size=(110, 20), font=('Helvetica 10'))],
            [
                sg.Multiline(size=(70, 5), enter_submits=True, key='-QUERY-', do_not_clear=False),
                sg.Button('SEND', button_color=(sg.YELLOWS[0], sg.BLUES[0]), bind_return_key=True),
                sg.Button('EXIT', button_color=(sg.YELLOWS[0], sg.GREENS[0]))
            ]
        ]

        self.window =  sg.Window('Chat window', layout, font=('Helvetica', ' 13'), default_button_element_size=(8,2))

    def start(self):
        while True:
            self.event, self.values = self.window.Read()
            if self.event == 'SEND':
                query = self.values['-QUERY-'].rstrip()
                if query:
                    data = f'@{username}: {query}'
                    user.send(data)
                    print(data)

            if self.event in (sg.WIN_CLOSED, 'EXIT'):
                break

        self.close()

    def close(self):
        self.window.close()

telaConnect = Login()
telaConnect.start()

telaChat = Chat()

rec = client.Receiver(user)
rec.start()

telaChat.start()

os._exit(0)