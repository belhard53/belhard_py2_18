import socket

# HOST = socket.gethostname()
# print(HOST)



def send_file(file_name, conn):
    try:
        with open(file_name.lstrip('/'), 'rb') as f:                   
            print(f"send file {file_name}")
            conn.send(OK)
            conn.send(HEADERS)
            conn.send(f.read())
            
    except IOError:
        print('нет файла')
        conn.send(ERR_404)
        

def is_file(path):       
    if '.' in path:
        ext =  path.split(".")[-1]
        if ext in ['jpg','png','gif', 'ico', 'txt', 'html', 'json']:
            return True
    return False




HOST = ('127.0.0.1', 7777)

# SOCK_DGRAM - UDP,  SOCK_STREAM - TCP, AF_INET - ip v4
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(HOST)
sock.listen()



# HTTP - запрос
# GET /project1/test1/ HTTP/1.1 - первая строка определяющая что это http - 
#                      3 параметра разделенные пробелом (тип путь протокол)
# Host: some.ru - 2я и последующие строки заголовки
# 1 пустые строки
# тело запроса(служебные данные)


# HTTP - ответ аналогичный - первая строка/хидеры/контент
# HTTP/1.1 200 OK
# Date: Thu, 29 Jul 2021 19:20:01 GMT
# Content-Type: text/html; charset=utf-8

# контент



print("--start--")

# conn, addr = sock.accept()    

OK = b'HTTP/1.1 200 OK\n'
HEADERS = b"Host: some.ru\nHost1: some1.ru\nContent-Type: text/html; charset=utf-8\n\n"
ERR_404 = b'HTTP/1.1 404 Not Found\n\n'


while True:
    print("---listen----")
    conn, addr = sock.accept()
    data = conn.recv(4096).decode()
    print(data)
    
    try:
        # тут так же можно добавить проверку есть ли в 1ой строке  "HTTP/1.1"
        method, path, ver  = data.split('\n')[0].split(" ", 2) # получаем path из 1ой строки http                        
        print('-----', method, path, ver)
        if "?" in path:
            # узнаем есть ли параметры
            path, params = path.split("?", 1)
            
        if is_file(path):
            # если известный файл возвращаем файл
            # таким образом будет уже отправляться браузеру favicon.ico
            send_file(path, conn) #можно  запросить любой файл html или картинку
            # http://127.0.0.1:7777/1.html
            # http://127.0.0.1:7777/doc.txt
            # http://127.0.0.1:7777/cat.jpg
            # http://127.0.0.1:7777/users.json
        else:
            if path == '/':
                # если главная страница открываем 1.html
                send_file('1.html', conn)
            elif path == '/test1/':
                html = "<h1> ТЕСТ 1 </h1>"
                conn.send(OK)
                conn.send(HEADERS)
                conn.send(html.encode())
                
            else:
                # во всех остальных случаях - 404
                conn.send(ERR_404)
                
            
    except:
        # грубо и условно но тут можно и так - это не рабочий пример
        conn.send(b'--------no http----------')
        
    conn.close()