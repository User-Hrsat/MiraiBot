class Ping:
    command = 'ping'
    usage = '就是ping嘛'

    def __init__(self):
        ...

    def __call__(self, addr):
        return 'text', f'Pong {addr[0]}'

    def __del__(self):
        ...
