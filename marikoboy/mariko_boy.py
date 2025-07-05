from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PIL import Image

from os.path import exists, join
from time import time

from flask import current_app
from pyboy import PyBoy
from pyboy.utils import WindowEvent as we

from marikoboy.config import ROMS_PATH

key_map = {
    14: [we.RELEASE_ARROW_LEFT, we.PRESS_ARROW_LEFT],
    15: [we.RELEASE_ARROW_RIGHT, we.PRESS_ARROW_RIGHT],
    12: [we.RELEASE_ARROW_UP, we.PRESS_ARROW_UP],
    13: [we.RELEASE_ARROW_DOWN, we.PRESS_ARROW_DOWN],
    1: [we.RELEASE_BUTTON_A, we.PRESS_BUTTON_A],
    2: [we.RELEASE_BUTTON_B, we.PRESS_BUTTON_B],  # Switch Y button
    5: [we.RELEASE_BUTTON_START, we.PRESS_BUTTON_START],  # Switch SR button
    7: [we.RELEASE_BUTTON_SELECT, we.PRESS_BUTTON_SELECT],  # Switch SL button
}


class Game(PyBoy):
    rom = None

    def __init__(self, rom: str):
        rom_path = join(ROMS_PATH, rom)
        if not exists(rom_path):
            raise IOError(f"File {rom_path} does not exist")
        super().__init__(rom_path, window="null", scale=1, sound_emulated=False)
        self.fps_time = time()
        self.start_time = time()
        self.rom = rom
        self.first_loop = True
        self.image_quality = 100  # Experimental
        self.skip = 0  # Experimental
        self.frameskip = False  # Experimental
        self.avg_fps = 60  # Need to be 60 for the first second so it won't trigger frameskip immediately
        self.fps = 60
        self.max_fps_collection = 30  # keep the last 30 calculated fps value (so 30s)
        self.fps_index = 0
        self.fps_time = 0.0
        self.collected_fps = [60 for _ in range(self.max_fps_collection)]

    def update_key(self, buttons: list):
        for button, pressed in enumerate(buttons):
            action = key_map.get(button)
            if action:
                current_app.logger.debug(f"Button:{button}\tAction:{we(action[int(pressed)])}")
                action = action[int(pressed)]
                current_app.logger.info(f"Updating key: {action}")
                self.send_input(action)
            else:
                current_app.logger.info(f"Button not mapped {button}")

    def update(self, framerate: bool = False):
        if time() - self.fps_time < 1.0:  # Checking if it's elapsed a second
            self.fps = self.fps + 1
        else:
            self.collected_fps[self.fps_index % self.max_fps_collection] = self.fps
            self.fps_index += 1
            if framerate:
                current_app.logger.info(f"FPS: {self.fps}\tFrame Skip: {self.frameskip}")
            if not self.first_loop:
                self.avg_fps = sum(self.collected_fps) / self.max_fps_collection
            else:
                self.avg_fps = sum(self.collected_fps) / self.fps_index
                self.first_loop = not (self.fps_index < self.max_fps_collection)
            self.fps_time = time()
            self.fps = 1
        self.tick()

    def get_frame(self) -> Image:
        return super().screen.image
