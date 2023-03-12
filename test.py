import socket

# Задаємо адресу та порт, до якого потрібно відправити запит
host = '192.168.0.109'
port = 80

# Створюємо об'єкт сокету
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Відправляємо запит на сервер за допомогою методу connect()
client_socket.connect((host, port))

# Відправляємо дані на сервер за допомогою методу sendall()
client_socket.sendall(b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n')

# Отримуємо відповідь від сервера за допомогою методу recv()
response = client_socket.recv(4096)

# Виводимо отриману відповідь
print(response.decode())

# Закриваємо з'єднання
client_socket.close()
