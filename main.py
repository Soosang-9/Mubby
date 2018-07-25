from os import system

from __process.logging_process import *
from __process.request_process import RequestProcess
from __process.schedule_process import Scheduling


class Main:
    def __init__(self):
        tcp_server = RequestProcess()
        # tcp_server.daemon = True

        # logging process 적용 해야 한다.
        # Scheduling()

        tcp_server.start()


if __name__ == "__main__":
    main = Main()
