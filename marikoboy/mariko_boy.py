#!/usr/bin/env python3

import os 
from time import time, sleep
from marikoboy.mgba import core, image, gba
import logging 
from threading import Thread

class Game():
    c = None 
    i = None
    thread = None
    running = False

    image_quality = 100 # Experimental
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


    def get_keys(self, pressed):
        binds = [   (14, gba.GBA.KEY_LEFT),\
                    (15, gba.GBA.KEY_RIGHT),\
                    (12, gba.GBA.KEY_UP),\
                    (13, gba.GBA.KEY_DOWN),\
                    (1, gba.GBA.KEY_A),\
                    (2, gba.GBA.KEY_B),\
                    (5, gba.GBA.KEY_START),\
                    (7, gba.GBA.KEY_SELECT)\
                ]
        return [j for (i,j) in binds if pressed[i]]


    def update_key(self, pressed):
        self.c.set_keys(*(self.get_keys(pressed)))
        return None


    def get_frame(self):
        return self.i.to_pil()


    def stop(self):
        self.c.reset()
        self.running = False
