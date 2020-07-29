import face_recognition, os, json, socket
from picamera import PiCamera
import numpy as np

# Global vars
ip = "192.168.0.10"
port = 4444

camera = PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

print("[+] Loading known images...")
known_faces = {}
for pic in os.listdir("known"):
    image = face_recognition.load_image_file("known/" + pic)
    known_faces[os.path.splitext(pic)[0]] = face_recognition.face_encodings(image)[0]

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect((ip, port))

def reliable_send(data):
        json_data = json.dumps(data)
        connection.send(json_data.encode())

while True:
    try:
        print("[+] Taking picture...")
        camera.capture(output, format="rgb")

        face_locations = face_recognition.face_locations(output)
        print("[+] Found {} faces".format(len(face_locations)))
        face_encodings = face_recognition.face_encodings(output, face_locations)

        for unknown in face_encodings:
            for name, known_face in known_faces.items():
                result = face_recognition.compare_faces([known_face], unknown)

                if result[0]:
                    print("[!] Found {}".format(name))
                    reliable_send("{}".format(name))
                else:
                    reliable_send("Unknown entity")
    except Exception as e:
        connection.close()
        print(e)
        break