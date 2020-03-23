 #!/usr/bin/env python3
from flask import Flask, request, redirect, url_for, render_template, send_file
from marikoboy import app, socketio
from flask_socketio import emit
from marikoboy.mariko_boy import Game
from time import time
import io
import os

game = None

# @socketio.on("gamepad_axis", namespace="/key_update")
# def gamepad_axis(axis):
#   TODO not necessary right now


@socketio.on('frame', namespace='/game')
def frame():
    if game:
        if game.frameskip:
            game.skip = 1 - game.skip
        if not game.skip:
            img = io.BytesIO()
            frame = game.get_frame().convert("RGB")
            
            frame.save(img, format="JPEG", optimize=True, progressive=True, subsampling=0, quality=game.image_quality)
            emit('update', {'image': True, 'buff':img.getvalue()})


@socketio.on("gamepad_button", namespace="/game")
def gamepad_button(pressed):
    if game and pressed:
        game.update_key(pressed)


@app.route("/streaming/", methods=['GET', 'POST'])
def streaming():
    if game:
        return render_template("streaming.html")
    return redirect(url_for("home"))


@app.route("/")
@app.route("/home")
def home():
    games = filter(lambda x : x.endswith("gb") or x.endswith("gbc") or x.endswith("gba"), os.listdir("marikoboy/roms"))
    return render_template("home.html", active_game=game, games=games)


@app.route("/start/<string:rom>", methods=['GET', 'POST'])
def start(rom):
    global game
    if game:
        game.stop()
    game = Game("marikoboy/roms/", rom)
    return redirect(url_for("streaming"))