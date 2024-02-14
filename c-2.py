# Client 4 code 
import socket
import json


    
def send_text_file(file_name, key, new_file_name):
    with open(file_name, "rb") as f:
        file_content = f.read()
        
    file_data = {
        "file_name": new_file_name,
        "file_content": file_content.decode('utf-8'),
        "Type": "SEND_FILE",
        "KEY": key
    }
    
    json_file_obj = json.dumps(file_data)
    
    client_socket.sendall(json_file_obj.encode('utf-8'))
    
    response = client_socket.recv(1024).decode('utf-8')
    content = json.loads(response)
    print(response)
    client_socket.close()
    
def send_file_name(file_name):
    client_socket.send(file_name.encode('utf-8'))
    
def send_file(file_name):
    print(file_name)
    send_file_name(file_name)
    with open(file_name, "rb") as f:
        file_content = f.read()
    client_socket.sendall(file_content)
    response = client_socket.recv(1024).decode('utf-8')
    content = json.loads(response)
    print(response)
    client_socket.close()
    
    
def receive_json_file(conn, new_file_name):
    json_data = conn.recv(1024)
    
    try:
        file_data = json.loads(json_data.decode('utf-8'))
        # print(file_data)

        file_name = file_data["file_name"]
        status = file_data["status"]
    
        print(f"file_name: {file_name}, status: {status}, From: {file_data['FROM']}")
        
        with open(new_file_name, "wb") as f:
            f.write(file_data['file_content'].encode('utf-8'))
        
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)

    

def request_file(file_name, conn, new_file_name, key=0):
    
    file_data = {
        "file_name": file_name,
        "Type": "REQUEST_FILE",
        "KEY": key,
        "FROM": "CLIENT"
    }
    request = json.dumps(file_data)
    
    conn.sendall(request.encode('utf-8'))
    
    # print(conn.recv(1024))
    receive_json_file(conn, new_file_name)


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_port = 12000

server_address = ('localhost', server_port)

client_socket.connect(server_address)

send_file("code.py")


