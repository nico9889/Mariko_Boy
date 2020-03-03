# MarikoBoy
Nothing to see here, I'm **not** actively mantaining this, I'm just doing experiment in my free time.
Also I'm a newbie.

## What is this?
This permit you to play GB/GBC homebrew in non-modified Nintendo Switch through the hidden browser.
This is deeply inspired by [z80z80z80's MarikoDoom](https://github.com/z80z80z80/MarikoDoom).

## How does this work?
This is based on [PyBoy Emulator](https://github.com/Baekalfen/PyBoy) and [Flask](https://github.com/pallets/flask). 
The console ask to the server for frame, the Python server get the frame from PyBoy and send this to the console through Flask. The game get updated as the frame get sent.

## How are the performance?
If you manage to get this to work, **you will regret**. I couldn't manage to get stable fps, this runs more or less on 10fps average on Nintendo Switch.
If you try this on the host machine through the local browser you will notice that this run at 60fps, probably the console can't manage all that image update or something.

# Known bugs
* ~~As of the last complete rewrite the server doesn't receive key updates from console correctly so it's literally unplayable 😎👍.~~  **Fixed [here](https://github.com/nico9889/Mariko_Boy/tree/socketio-full)**
* ~~Poor framerate on Nintendo Switch~~  **Partly fixed [here](https://github.com/nico9889/Mariko_Boy/tree/socketio-full)**
* Missing audio (at the time of writing PyBoy doesn't support audio).

# Can you add ...?
**No.** I started developing this just for fun. I don't even know if I will continue supporting this.

# How can I run this?
Install [PyBoy Emulator](https://github.com/Baekalfen/PyBoy) and [Flask](https://github.com/pallets/flask).
Put your GB/GBC file in the roms folder, start the server (python run.py) and connect to your computer through SwitchBru DNS.
If you don't know what I'm talking about, please use Google, since this is not intended for daily usage.
