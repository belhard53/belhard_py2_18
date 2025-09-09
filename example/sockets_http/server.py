import socket

# HOST = socket.gethostname()
# print(HOST)

HOST = ('127.0.0.1', 7777)

# SOCK_DGRAM - UDP,  SOCK_STREAM - TCP, AF_INET - ip v4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(HOST)
sock.listen()

print("--start--")

while 1:
    print("---listen----")
    conn, addr = sock.accept()    
    # print(conn)
    # print(addr)
    
    
    # ------------------------
    # получит все данные но не более 1024 байт
    data = conn.recv(1024).decode()
    print(data)
    conn.send(f"Данные получены - {data[::-1]}".encode())    
    
    
    # # ----------------------------
    # # получит только 4 байта, неважно send или sendall
    # data = conn.recv(4).decode()
    # print(data)
    # conn.send(f"Данные получены - {data[::-1]}".encode())  

    if data == 'stop':
            break

print("--end--")
