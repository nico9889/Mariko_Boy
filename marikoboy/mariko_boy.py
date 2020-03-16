#!/usr/bin/env python3

import os 
from time import time, sleep
from marikoboy.mgba import core, image
import logging 
from threading import Thread
import numpy as np


class Game():
    c = None 
    i = None
    thread = None
    running = False

    image_quality = 50 # Experimental
    skip = 0            # Experimental
    frameskip = True   # Experimental
    rom = None

    def run(self):
        while self.running:
            self.c.run_frame()
            sleep(1/60)

    def __init__(self, path, rom):
        if os.path.exists(path + rom):
            self.c = core.load_path(path+rom)
            self.i=image.Image(*self.c.desired_video_dimensions())
            self.c.set_video_buffer(self.i)
            self.c.reset()
            self.thread = Thread(target=self.run)
            self.fps_time = time()
            self.start_time = time()
            self.rom = rom
            self.running = True
            self.thread.start()
            
        else:
            raise IOError

    '''
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
    '''

    def update_key(self, pressed):
        '''
        for button in range(len(pressed)):
            action = self.get_action(button, pressed[button])
            if(action):
                self.send_input(action)
        '''
        return None


    def update(self, framerate = False):
        '''
        if(time()-self.fps_time<1.0):   # Checking if it's elapsed a second 
            self.fps = self.fps + 1
        else:
            if framerate:
                print("FPS: " + str(self.fps) + " Frameskip: " + str(self.frameskip))
            self.fps_sum = self.fps_sum + self.fps
            self.avg_fps = round(self.fps_sum/(time()-self.start_time))
            self.fps_time = time()
            self.fps = 0
        '''
        self.c.run_frame()

    def get_frame(self):
        return self.i.to_pil()

    def get_audio(self):
        return self.c.get_audio_channels().read(44100)

    def stop(self):
        self.c.reset()
        self.running = False
