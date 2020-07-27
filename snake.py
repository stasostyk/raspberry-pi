from sense_hat import SenseHat
import random
import time

sense = SenseHat()

cherry_map = []
snake_map = []
head = [3,3]
direction = "waiting"

def spawn_cherry():
    cherry_map.append([random.randrange(7), random.randrange(7)])


if __name__ == '__main__':
    spawn_cherry()

    while True:
        # if direction == "waiting":
        #     continue
#moving

        time.sleep(0.5)

        snake_map.append([head[0], head[1]])

        acceleration = sense.get_accelerometer_raw()

        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']

        x=round(x, 0)
        y=round(y, 0)
        z=round(z, 0)

        if x  == -1:
            head[0]-=1
        elif y == 1:
            head[1]+=1
        elif y == -1:
            head[1]-=1
        else:
            head[0]+=1

# checking
        x, y = head
        lost = False
        if x <= -1 or x >= 8 or y <= -1 or y >= 8:
            print("You walked into the wall")
            lost = True
        for x2, y2 in snake_map:
            if x == x2 and y == y2:
                print("You ate yourself")
                lost = True
        if lost:
            sense.clear(50,0,0)
            time.sleep(1)
            sense.clear()
            break

        eaten = False
        for x2, y2 in cherry_map:
            if x == x2 and y == y2:
                del cherry_map[0]
                spawn_cherry()
                eaten = True
        if not eaten:
            del snake_map[0]

#drawing
        sense.clear()
        sense.set_pixel(head[0], head[1], (0,70,150))
        for pos in snake_map:
            sense.set_pixel(pos[0], pos[1], (0,70,150))

        for pos in cherry_map:
            sense.set_pixel(pos[0], pos[1], (150,0,0))