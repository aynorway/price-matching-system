"""
This script runs the price_matching_system application using a development server.
"""

from os import environ
from price_matching_system import create_app

class RunServer:

    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT

    def start_server(self):
        create_app().run(self.HOST, self.PORT)

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    RunServer(HOST, PORT).start_server()
