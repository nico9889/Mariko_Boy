#!/usr/bin/env python3

import os 
from time import time
from pyboy import PyBoy, logger
import pyboy.windowevent as WE
import logging 


class Game(PyBoy):
    avg_fps = 60        # Need to be 60 for the first second so it won't trigger frameskip immediatly
    fps = 60
    fps_sum = 0
    fps_time = 0.0
    start_time = 0.0

    image_quality = 100 # Experimental
    skip = 0            # Experimental
    frameskip = False   # Experimental
    rom = None


    def __init__(self, path, rom):
        if os.path.exists(path + rom):
            super().__init__(path + rom, window_type="headless", window_scale=1)
            self.fps_time = time()
            self.start_time = time()
            self.rom = rom
        else:
            raise IOError


    def get_action(self, key, pressed):
        if key == 14 and pressed: # MOVE_LEFT
            action = WE.PRESS_ARROW_LEFT
        elif key == 14 and not pressed: 
            action = WE.RELEASE_ARROW_LEFT
        elif key == 15 and pressed: # MOVE_RIGHT
            action = WE.PRESS_ARROW_RIGHT
        elif key == 15 and not pressed: 
            action = WE.RELEASE_ARROW_RIGHT
        elif key == 12 and pressed: # MOVE_FORWARD
            action = WE.PRESS_ARROW_UP
        elif key == 12 and not pressed: 
            action = WE.RELEASE_ARROW_UP
        elif key == 13 and pressed: # MOVE_BACKWARD
            action = WE.PRESS_ARROW_DOWN
        elif key == 13 and not pressed: 
            action = WE.RELEASE_ARROW_DOWN
        elif key == 1 and pressed: # BUTTON A
            action = WE.PRESS_BUTTON_A
        elif key == 1 and not pressed: 
            action = WE.RELEASE_BUTTON_A
        elif key == 2 and pressed: # BUTTON B (Y Switch Button)
            action = WE.PRESS_BUTTON_B
        elif key == 2 and not pressed: 
            action = WE.RELEASE_BUTTON_B
        elif key == 5 and pressed: # START (SR Switch Button)
            action = WE.PRESS_BUTTON_START
        elif key == 5 and not pressed: 
            action = WE.RELEASE_BUTTON_START
        elif key == 7 and pressed: # SELECT (SL Switch Button)
            action = WE.PRESS_BUTTON_SELECT
        elif key == 7 and not pressed: 
            action = WE.RELEASE_BUTTON_SELECT
        else:
            action = None
        return action


    def update_key(self, pressed):
        for button in range(len(pressed)):
            action = self.get_action(button, pressed[button])
            if(action):
                self.send_input(action)


    def update(self, framerate = False):
        if(time()-self.fps_time<1.0):   # Checking if it's elapsed a second 
            self.fps = self.fps + 1
        else:
            if framerate:
                print("FPS: " + str(self.fps) + " Frameskip: " + str(self.frameskip))
            self.fps_sum = self.fps_sum + self.fps
            self.avg_fps = round(self.fps_sum/(time()-self.start_time))
            self.fps_time = time()
            self.fps = 0

        self.tick()

    def get_frame(self):
        return self.get_screen_image()

    

    

