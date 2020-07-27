from sense_hat import SenseHat
sense = SenseHat()

while True:
    acceleration = sense.get_accelerometer_raw()
    
    x = round(acceleration['x'] * 4, 0) +3
    y = round(acceleration['y'] * 4, 0) +3

    if x>7:
        x = 7
    elif x<0:
        x=0
    if y>7:
        y = 7
    elif y<0:
        y=0
    sense.clear()
    sense.set_pixel(int(x), int(y), (0,60,150))
    print(x)
    print(y)
    print("===")

    