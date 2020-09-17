# raspberry-pi
An archive of public python scripts for the raspberry pi, open to changes and use, especially in terms of learning the various capabilities of the Pi and some of its extensions.
#### Note
The listener files have to be ran on the computer/ device, and the other file on the Pi. Also change the port and IP variables at the top of the files.

## Sense Hat (sense_hat)
* displayEditor - A PyGame powered editor for the sense hat 8x8 display.
* plate - a visual simulation of gravity, representing a ball on the display, using the accelerometer.
* snake - the popular snake game on the hat display, using orientation to move around (accelerometer).
* gyrostick & gyrostick_listener - utilizing the Pi's orientation as a mouse, using joystick (slowly moving) mechanics.
* gyromouse & gyromouse_listener - similar to the gyrostick, except the position on the theoretical zy plane is directly reflected onto the mouse on the screen.
* clear - clears the 8x8 sense hat display.
#### Dependencies
```
pip install sense_hat, sockets
```

## Camera (picamera)
* TCP_face_recognizer & TCP_face_listener - Rpi scans for faces, then notifies you on your desktop screen notification
Create a folder called known, and add pictures of known faces with their names in the file name. Change your 'ip' and 'port' variables, and get started! Relies on a TCP connection, so run on both devices
#### Dependencies
``` 
pip3 install face_recognition, sockets, picamera, numpy
```
