import socket

# HOST = socket.gethostname()
# print(HOST)

HOST = ('127.0.0.1', 7777)

# SOCK_DGRAM - UDP,  SOCK_STREAM - TCP, AF_INET - ip v4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(HOST)
sock.listen()


# sock.settimeout(1)

print("--start--")

# conn, addr = sock.accept()    

while 1:
    print("---listen----")
    conn, addr = sock.accept()    
    # print(conn)
    # print(addr)
    
    
    # ------------------------
    # получит все данные но не более 1024 байт
    data = conn.recv(1024).decode()
    print(data)
    # conn.send(f"Данные получены - {data[::-1]}".encode())    
    conn.send(f"12345".encode())    
    
    # 
    # # ----------------------------
    # # получит только 4 байта, неважно send или sendall
    # data = conn.recv(4).decode()
    # print(data)
    # conn.send(f"Данные получены - {data[::-1]}".encode())  


    # # -----------------------------    
    # # для получения данных частями например по 2 байта    
    # while True:
    #     data = conn.recv(2) # если соединение не закрыто клиентом залипает на этой строчке                
    #     if not data:            
    #         break
    #     print(data)



    if data == 'stop':
            break
        
    

print("--end--")




# def receive_all(sock, buffer_size=4096):
#     """Получить все данные до закрытия соединения"""
#     data = b''
#     while True:
#         chunk = sock.recv(buffer_size)
#         if not chunk:  # Пустые данные = соединение закрыто
#             break
#         data += chunk
#     return data

# def receive_all(sock, size):
#     """Получить точно size байт"""
#     data = b''
#     while len(data) < size:
#         chunk = sock.recv(min(size - len(data), 4096))
#         if not chunk:
#             break
#         data += chunk
#     return data



# recv() переходит к следующей строке когда:
#     Пришли данные (любое количество)
#     Соединение закрыто (data = b'')
#     Произошла ошибка (исключение)
#     Истек таймаут (если установлен)