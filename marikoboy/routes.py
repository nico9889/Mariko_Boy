 #!/usr/bin/env python3
from flask import Flask, request, redirect, url_for, render_template, send_file
from marikoboy import app, socketio
from marikoboy.mariko_boy import Game
from time import time
import io
import os


active_game = None


# @socketio.on("gamepad_axis", namespace="/key_update")
# def gamepad_axis(axis):
#   TODO not necessary right now


@socketio.on("gamepad_button", namespace="/key_update")
def gamepad_button(pressed):
    if active_game:
        active_game.update_key(pressed)


@app.route("/img.jpg")
def img():
    # print(str(time()) + " Auto-Frame Update")
    img = io.BytesIO()
    frame = active_game.update(framerate=1)
    frame.save(img, format="JPEG", subsampling=0, quality=100)
    img.seek(0)
    return send_file(img, mimetype='image/JPEG')


@app.route("/streaming/", methods=['GET', 'POST'])
def streaming():
    if active_game:
        return render_template("streaming.html")
    return redirect(url_for("home"))


@app.route("/")
@app.route("/home")
def home():
    games = filter(lambda x : x.endswith("gb") or x.endswith("gbc"), os.listdir("marikoboy/roms"))
    return render_template("home.html", active_game=active_game, games=games)


@app.route("/start/<string:game>", methods=['GET', 'POST'])
def start(game):
    global active_game
    if active_game:
        active_game.stop()
    active_game = Game("marikoboy/roms/", game)
    return redirect(url_for("streaming"))