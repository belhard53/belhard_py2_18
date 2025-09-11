import socket


HOST = ('127.0.0.1', 7777)

# SOCK_DGRAM - UDP,  SOCK_STREAM - TCP, AF_INET - ip v4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


sock.connect(HOST)

# l = sock.send(b'0123456789')
# sock.send('0123456789'.encode())
# sock.send('0123456789 Hello Вася'.encode("utf-8")) # отправляет столько сколько принимают
sock.send('0123456789 Hello Вася'.encode("utf-8")) # отправляет все
data = sock.recv(1024).decode() # ждем отправки ответа
print(data) # печатаем ответ


# ===================================
# если сервер принимает маленькими пакетами например по 2 байта
# отправляем до  тех пор пока все не примут
# send_data = b"0123456789 Hello Вася"
# sent = 0
# while sent < len(send_data):
#     sent = sent + sock.send(send_data[sent:])
    
# sock.close()    