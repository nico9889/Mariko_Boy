#!/usr/bin/env python3

import os 
from time import time
from pyboy import PyBoy
import pyboy.windowevent as WE

class Game(PyBoy):
    fps = 0
    time = 0.0
    rom = None

    def __init__(self, path, rom):
        if os.path.exists(path + rom):
            super().__init__(path + rom, window_type="headless")
            self.time = time()
            self.rom = rom
        else:
            raise IOError
    
    def get_action(self, data):
        if data == "INIT":
            print(" * Client connected.")
            action = None
            data = 0
        elif data == "left_down": # MOVE_LEFT
            action = WE.PRESS_ARROW_LEFT
        elif data == "left_up": 
            action = WE.RELEASE_ARROW_LEFT
        elif data == "right_down": # MOVE_RIGHT
            action = WE.PRESS_ARROW_RIGHT
        elif data == "right_up": 
            action = WE.RELEASE_ARROW_RIGHT
        elif data == "up_down": # MOVE_FORWARD
            action = WE.PRESS_ARROW_UP
        elif data == "up_up": 
            action = WE.RELEASE_ARROW_UP
        elif data == "down_down": # MOVE_BACKWARD
            action = WE.PRESS_ARROW_DOWN
        elif data == "down_up": 
            action = WE.RELEASE_ARROW_DOWN
        elif data == "a_down": # BUTTON A
            action = WE.PRESS_BUTTON_A
        elif data == "a_up": 
            action = WE.RELEASE_BUTTON_A
        elif data == "y_down": # BUTTON B
            action = WE.PRESS_BUTTON_B
        elif data == "y_up": 
            action = WE.RELEASE_BUTTON_B
        elif data == "sr_down": # START 
            action = WE.PRESS_BUTTON_START
        elif data == "sr_up": 
            action = WE.RELEASE_BUTTON_START
        elif data == "sl_down": # SELECT
            action = WE.PRESS_BUTTON_SELECT
        elif data == "sl_up": 
            action = WE.RELEASE_BUTTON_SELECT
        else:
            action = None
        return action

    def update_key(self, key):
        if key:
            action = self.get_action(key)
            if action:
                self.send_input(action)

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


    

    

