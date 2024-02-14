import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_port = 12000

server_address = ('localhost', server_port)

client_socket.connect(server_address)

file_name = "send.txt"

with open(file_name, "rb") as f:
    file_content = f.read()
    
data = file_name.encode('utf-8') + b'##' + file_content

# print(data)

client_socket.sendall(data)


client_socket.close()
