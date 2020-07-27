from sense_hat import SenseHat
import socket, json, time

# global vars
ip = "192.168.0.3"
port = 4444

sense = SenseHat()

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((ip, port))

mouse_button = "None"

def reliable_send(data):
        json_data = json.dumps(data)
        connection.send(json_data)

def stick_controll(event):
    global mouse_button
    if event.action == 'pressed':
        if event.direction == 'up':
            print("[+] Right clicking...")
            mouse_button = "right"
        elif event.direction == 'down':
            print("[+] Left clicking...")
            mouse_button = "left"

sense.stick.direction_any = stick_controll

while True:
    try:
        acceleration = sense.get_accelerometer_raw()
        y = round(acceleration['y'] * 540, 0)-540 #converting xy plane to screen display
        z = round(acceleration['z'] * 960, 0)+960
        y*=-1
        

        # print("y={0}, z={1}".format(y,z))

        reliable_send("{0}:{1}:{2}".format(z,y, mouse_button).encode())
        mouse_button = "None"
        time.sleep(1)
    except:
        connection.close()
        print("[-] Closing...")
        break