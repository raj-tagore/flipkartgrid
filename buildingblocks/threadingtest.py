from threading import Thread
import time


def a():
    for i in range(1000):
        print(i)
        time.sleep(1)


def b():
    for i in range(1000):
        print(i)
        time.sleep(3)


if __name__ == '__main__':
    a1 = Thread(target=a)
    b2 = Thread(target=b)
    a1.start()
    b2.start()
