import socket
import threading
import json

ENCODE_TYPE = "utf-8"
PREFIX = ['txt', 'c', 'py', 'cpp']
FILE_NAME = ''

def is_json(data):
    try:
        json.loads(data)
        return True
    except ValueError:
        return False

def send_request_file(file_name, conn):
    print("send_request_file")
    with open(file_name, "rb") as f:
        file_content = f.read()
        
    file_data = {
        "file_name": file_name,
        "file_content": file_content.decode(ENCODE_TYPE),
        "Type": "RESPONSE",
        "status": 200,
        "phrase": "OK",
        "FROM": "SERVER"
    }
    
    json_file_obj = json.dumps(file_data)
        
    # print(f"file_data : {file_data}")
    # print(f"json_file_obj : {json_file_obj}")
    
    conn.sendall(json_file_obj.encode(ENCODE_TYPE))


def handle_client_connection(conn, addr):
    print(f"Connection from {addr}")
    data = b""
    # print("after data")
    while True:
        chunk = conn.recv(1024)
        # print(chunk)
        if len(chunk) < 1024:
            data += chunk
            break
        data += chunk
    # json_data = data.decode(ENCODE_TYPE)
    json_data = data
    # print("json_data: "+json_data)
    # print("after json_data")
    if is_json(data):
        # print("is_json")
        json_data = json.loads(json_data)
        file_name = json_data['file_name']
        if json_data['Type'] == "SEND_FILE":
            # print("SEND_FILE")
            if file_name.endswith('.txt'):
                # print(".txt")
                receive_text_file(conn, json_data)
            else:
                print("Unsupported file type")
        elif json_data['Type'] == "REQUEST_FILE":
            send_request_file(file_name, conn)
        conn.sendall("Received the file successfully!".encode(ENCODE_TYPE))
    else:
        # print("receive_file")
        receive_file(conn, data)
    conn.close()


  
def receive_text_file(conn, json_data):
    file_name = json_data['file_name']
    file_content = json_data['file_content']
    
    with open(file_name, "wb") as f:
        f.write(file_content.encode(ENCODE_TYPE))
        
    response = {
        "file_name": file_name,
        "Type": "RESPONSE",
        "status": 200,
        "phrase": "OK",
        "FROM": "SERVER"
    }
    conn.sendall(json.dumps(response).encode(ENCODE_TYPE))


def receive_file(conn, data):
    # print(data)
    # FILE_NAME = ""
    # file_name = data.decode(ENCODE_TYPE).split('.')
    # if file_name[1] in PREFIX:
    #     global FILE_NAME = data
        
    
    with open('FILE.txt', "wb") as f:
        f.write(data)
        
    response = {
        "file_name": FILE_NAME,
        "Type": "RESPONSE",
        "status": 200,
        "phrase": "OK",
        "FROM": "SERVER"
    }
    conn.sendall(json.dumps(response).encode(ENCODE_TYPE))
    

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_port = 12000

server_address = ('localhost', server_port)

server_socket.bind(server_address)

server_socket.listen(5)

print("Server start !!")

while True:
    conn, cli_address = server_socket.accept()
    threading.Thread(target=handle_client_connection, args=(conn, cli_address)).start()
