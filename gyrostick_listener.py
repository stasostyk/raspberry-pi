import socket, json, pyautogui

ip = "192.168.0.3"
port = 4444

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind((ip, port))
listener.listen(0)
print("[+] Waiting for incoming connections")
connection, address = listener.accept()
print("[+] Got a connection from " + str(address))

prev_button = ""

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
        data = reliable_recieve().split(":")
        pyautogui.moveRel(int(float(data[0])), int(float(data[1]))*-1)
        if prev_button == data[2] == "left":
            pyautogui.doubleClick()
        elif data[2] == "left":
            pyautogui.click()
        elif data[2] == "right":
            pyautogui.click(button="right")
        prev_button = data[2]
        print(data)
    except:
        connection.close()
        print("[-] Closing...")
        break