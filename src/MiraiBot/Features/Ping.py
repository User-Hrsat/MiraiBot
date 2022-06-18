class Ping:
    command = 'ping'
    usage = '就是ping嘛'

    def __init__(self):
        print('Ping Init')

    def __call__(self, addr):
        return 'text', f'Ping {addr} ...'
