import time
import sys
from pathlib import Path

from CustomSocket import CustomSocket


def x():
    if getattr(sys, 'frozen', False):
        folder = Path(sys._MEIPASS)
    else:
        folder = Path(__file__).parent

    print(folder)

def test():

    sock = CustomSocket()
    sock.connect()
    data = []
    start = time.time()

    while True:
        message = sock.read_socket_buffer_for_port()
        datapoints = message.split('\n')
        data.extend(datapoints)
        if time.time()-start >= 10:
            break

        ret = [d for d in data if d != '']
    return ret


if __name__ == '__main__':
    print(sys._MEIPASS)
    x()
    quit()
    data = test()
    print(len(data))

