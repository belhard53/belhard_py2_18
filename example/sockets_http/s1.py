import socket

HOST = ('127.0.0.1', 8777)

# SOCK_DGRAM - UDP,  SOCK_STREAM - TCP, AF_INET - ip v4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(HOST)
sock.listen()



print("--start--")
print("---listen----")
conn, addr = sock.accept()  
print(conn)
data = conn.recv(2)
print(data)
data = conn.recv(2)
print(data)
data = conn.recv(2)
print(data)
data = conn.recv(2)
print(data)


print("end")

input()