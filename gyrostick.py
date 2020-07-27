from sense_hat import SenseHat
import socket, json, time

# global vars
SENSITIVITY = 150
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
    global SENSITIVITY
    if event.action == 'pressed':
        if event.direction == 'up':
            print("[+] Right clicking...")
            mouse_button = "right"
        elif event.direction == 'down':
            print("[+] Left clicking...")
            mouse_button = "left"
        elif event.direction == 'left':
            print("[+] Increasing sensitivity to {0}...".format(SENSITIVITY+20))
            SENSITIVITY+=20
        elif event.direction == 'right':
            print("[+] Decreasing sensitivity to {0}...".format(SENSITIVITY-20))
            SENSITIVITY-=20

sense.stick.direction_any = stick_controll

while True:
    try:
        acceleration = sense.get_accelerometer_raw()
        y = round(acceleration['y'] * SENSITIVITY, 0)
        z = round(acceleration['z'] * SENSITIVITY, 0)

        if y < 30 and y > -30: # eliminates tiny movements, caused by minor turbulances
            y = 0
        if z < 30 and z > -30:
            z = 0

        # print("y={0}, z={1}".format(y,z))

        reliable_send("{0}:{1}:{2}".format(z,y, mouse_button).encode())
        mouse_button = "None"
        time.sleep(1)
    except:
        connection.close()
        print("[-] Closing...")
        break