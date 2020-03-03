#!/usr/bin/env python3

import os 
from time import time
from pyboy import PyBoy
import pyboy.windowevent as WE

class Game(PyBoy):
    fps = 0
    time = 0.0
    rom = None
    pressed = []

    def __init__(self, path, rom):
        if os.path.exists(path + rom):
            super().__init__(path + rom, window_type="headless")
            self.time = time()
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
            if not self.pressed or pressed[button]!=self.pressed[button]:  # Updating key only when they change status
                action = self.get_action(button, pressed[button])
                self.send_input(action)
        self.pressed = pressed

    def update(self, framerate = 0):
        if framerate:
            if(time()-self.time<1.0):
                self.fps = self.fps + 1
            else:
                print("FPS: " + str(self.fps))
                self.time = time()
                self.fps = 0
        self.tick()
        frame = self.get_screen_image().convert("RGB")
        return frame


    

    

