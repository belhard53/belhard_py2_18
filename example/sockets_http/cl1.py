import socket



HOST = ('127.0.0.1', 8777)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(HOST)

snd_buf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
print(f"Размер буфера отправки: {snd_buf_size} байт")


l = sock.send(b'0123456789') # помещает в буфер
print('--->', l)

