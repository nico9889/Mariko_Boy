from os import getenv
from os.path import exists
from sys import exit

ROMS_PATH = getenv("MB_ROMS_PATH")

if not exists(ROMS_PATH):
    print("fSpecified PATH {ROMS_PATH} does not exist}")
    exit(-1)