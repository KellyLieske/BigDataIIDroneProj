import sys
import threading
import traceback

import av
import cv2
import numpy
import tellopy
import pygame
import time
import pygame.locals

#adapted from https://github.com/hanyazou/TelloPy/blob/develop-0.7.0/tellopy/examples/joystick_and_video.py

def recv_thread(drone):
    global run_recv_thread
    global new_image



    try:
        container = av.open(drone.get_video_stream())
        # skip first 300 frames
        frame_skip = 300
        while True:
            for frame in container.decode(video=0):
                if 0 < frame_skip:
                    frame_skip = frame_skip - 1
                    continue
                start_time = time.time()
                image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)


                new_image = image
                if frame.time_base < 1.0/60:
                    time_base = 1.0/60
                else:
                    time_base = frame.time_base
                frame_skip = int((time.time() - start_time)/time_base)
    except Exception as ex:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        print(ex)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #For xbox series X Controller
    global new_image
    pygame.init()
    pygame.joystick.init()
    current_image = None
    joy = pygame.joystick.Joystick(0)
    joy.init()
    print(joy.get_name())

    drone = tellopy.Tello()

    time.sleep(2)
    drone.connect()

    #drone.land()

    val = True

    leftStickUD = 1
    leftStickLR = 0

    rightStickUD = 2
    rightStickLR = 3

    buttonA = 0
    buttonB = 1
    buttonX = 2
    buttonY = 3

    buttonLB = 4
    buttonRB = 5

    buttonSt = 7
    buttonSl = 6

    threading.Thread(target=recv_thread, args=[drone]).start()

    while val:
        for event in pygame.event.get():
            if event.type == pygame.locals.JOYAXISMOTION:
                if event.axis == 1 and event.value > .95:
                    drone.backward(event.value * 15)
                elif event.axis == 1 and event.value < -.95:
                    drone.forward(event.value * -15)
                elif event.axis == 0 and event.value > .95:
                    drone.right(event.value * 15)
                elif event.axis == 0 and event.value < -.95:
                    drone.left(event.value * -15)

                #drone.left(0)
                #print(event)
            elif event.type == pygame.locals.JOYBUTTONDOWN:
                if event.button == 7:
                    drone.takeoff()
                elif event.button == 6:
                    drone.land()
            if current_image is not new_image:
                cv2.imshow('Tello', new_image)
                current_image = new_image
                cv2.waitKey(1)

                # print(event)



       # # for i in range(joy.get_numaxes()):
       #      print(str(i) + ": " + str(joy.get_axis(i)))
       #  for i in range(joy.get_numbuttons()):
       #      print(str(i) + ": " + str(joy.get_button(i)))
       #
       #  time.sleep(1)
       #  print(joy.get_numaxes())
       #  print(joy.get_numbuttons())











# See PyCharm help at https://www.jetbrains.com/help/pycharm/
