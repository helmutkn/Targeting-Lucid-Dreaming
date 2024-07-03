import time
from ZmaxHeadband import ZmaxHeadband
from line_profiler_pycharm import profile


@profile
def test():
    hb = ZmaxHeadband()
    reqID = [0, 1, 2, 3, 4]

    total_data = []
    start = time.time()
    while True:
        total_data.extend(hb.read(reqID))
        if time.time()-start >= 1:
            break
    return total_data


if __name__ == '__main__':
    data = test()
    print(len(data))


