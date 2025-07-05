from os import listdir

from flask import redirect, url_for, render_template, current_app
from flask_socketio import emit

from marikoboy import app, socketio
from marikoboy.config import ROMS_PATH
from marikoboy.mariko_boy import Game
from io import BytesIO

game: Game | None = None


@socketio.on('frame', namespace='/game')
def frame():
    if not game:
        return
    game.update(framerate=True)
    if game.frameskip:
        game.skip = 1 - game.skip

    # Skip a frame if the client is overwhelmed
    if game.skip:
        current_app.logger.warning("Skipping frame")
        return

    img = BytesIO()
    frame = game.get_frame().convert("RGB")

    # Experimental adaptive image quality based on avg framerate
    # I got this by trial&error
    # TODO: improve
    if game.avg_fps < 30:
        if game.image_quality >= 20:  # Limit minimum quality 10%
            game.image_quality = game.image_quality - 10
            game.frameskip = False
    elif game.fps > (game.avg_fps + 10) or game.avg_fps >= 59:
        if game.image_quality <= 90:  # Limit maximum quality 100%
            game.image_quality = game.image_quality + 5

    # Experimental auto-frame skip
    if game.avg_fps >= 59:
        game.frame_skip = False

    frame.save(img, format="webp", optimize=True, progressive=True, subsampling=0, quality=game.image_quality)

    emit('update', {'image': True, 'buff': img.getvalue()})


@socketio.on("gamepad_button", namespace="/game")
def gamepad_button(pressed: list[int]):
    if not game or not pressed:
        return
    game.update_key(pressed)


@app.route("/streaming/", methods=['GET', 'POST'])
def streaming():
    if not game:
        return redirect(url_for("home"))
    return render_template('streaming.html')


@app.route("/")
@app.route("/home")
def home():
    games = filter(lambda x: x.endswith("gb") or x.endswith("gbc"), listdir(ROMS_PATH))
    return render_template("home.html", active_game=game, games=games)


@app.route("/start/<string:rom>", methods=['GET', 'POST'])
def start(rom):
    global game
    if game:
        game.stop()
    game = Game(rom)
    return redirect(url_for("streaming"))
