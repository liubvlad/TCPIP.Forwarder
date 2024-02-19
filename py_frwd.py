import socket

def forward_tcp(local_port, remote_host, remote_port):
    # Создаем сокет для прослушивания входящих соединений
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_socket.bind(('localhost', local_port))
    local_socket.listen(1)
    
    print(f'Listening for connections on port {local_port}')
    
    while True:
        # Принимаем входящее подключение
        client_socket, client_addr = local_socket.accept()
        print(f'Accepted connection from {client_addr}')
        
        # Создаем сокет для подключения к удаленному серверу
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, remote_port))
        
        # Начинаем пересылку данных между клиентом и сервером
        while True:
            # Читаем данные от клиента и отправляем их на удаленный сервер
            data = client_socket.recv(4096)
            if not data:
                break
            remote_socket.sendall(data)
            
            # Читаем ответ от удаленного сервера и отправляем его клиенту
            data = remote_socket.recv(4096)
            if not data:
                break
            client_socket.sendall(data)
        
        # Закрываем соединения
        client_socket.close()
        remote_socket.close()

# Пример использования: перенаправляем порт 8888 локально на порт 80 удаленного сервера
forward_tcp(8888, 'example.com', 80)
