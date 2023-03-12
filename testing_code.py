import socket
import time
from threading import Thread

host = '192.168.0.109'
start_port = 1
end_port = 63000


def testing_port(a):
    for port in range(a, a + 101):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)  # Устанавливаем таймаут в полсекунды
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port} is open")
        sock.close()


def main():
    for i in range(int(end_port/100)+2):
        time.sleep(0.05)
        Thread(target=testing_port, args=(i*100,)).start()


main()
