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
    14: [we.RELEASE_ARROW_LEFT, we.PRESS_ARROW_LEFT ],
    15: [we.RELEASE_ARROW_RIGHT, we.PRESS_ARROW_RIGHT ],
    12: [we.RELEASE_ARROW_UP, we.PRESS_ARROW_UP ],
    13: [we.RELEASE_ARROW_DOWN, we.PRESS_ARROW_DOWN],
    1: [we.RELEASE_BUTTON_A, we.PRESS_BUTTON_A],
    2: [we.RELEASE_BUTTON_B, we.PRESS_BUTTON_B],  # Switch Y button
    5: [we.RELEASE_BUTTON_START, we.PRESS_BUTTON_START],  # Switch SR button
    7: [we.RELEASE_BUTTON_SELECT, we.PRESS_BUTTON_SELECT],  # Switch SL button
}


class Game(PyBoy):
    avg_fps = 60  # Need to be 60 for the first second so it won't trigger frameskip immediately
    fps = 60
    fps_sum = 0
    fps_time = 0.0
    start_time = 0.0

    image_quality = 100  # Experimental
    skip = 0  # Experimental
    frameskip = False  # Experimental
    rom = None

    def __init__(self, rom: str):
        rom_path = join(ROMS_PATH, rom)
        if not exists(rom_path):
            raise IOError(f"File {rom_path} does not exist")
        super().__init__(rom_path, window="null", scale=1)
        self.fps_time = time()
        self.start_time = time()
        self.rom = rom

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
            if framerate:
                current_app.logger.info(f"FPS: {self.fps}\tFrame Skip: {self.frameskip}")
            self.fps_sum = self.fps_sum + self.fps
            self.avg_fps = round(self.fps_sum / (time() - self.start_time))
            self.fps_time = time()
            self.fps = 0
        self.tick()

    def get_frame(self) -> Image:
        return super().screen.image
