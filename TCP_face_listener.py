import json, socket
from plyer import notification

ip = "192.168.0.10"
port = 4444

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind((ip, port))
listener.listen(0)
print("[+] Waiting for incoming connections")
connection, address = listener.accept()
print("[+] Got a connection from " + str(address))

def reliable_recieve():
    json_data = ""
    while True:
        try:
            json_data += connection.recv(1024).decode()
            return json.loads(json_data)
        except ValueError:
            continue

while True:
    try:
        data = reliable_recieve()
        notification.notify(title="Raspberry Pi", message=data+" has been found!", timeout=5)
        
    except Exception as e:
        connection.close()
        print(e)
        break
