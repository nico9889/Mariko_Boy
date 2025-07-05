const pressed = [];

// Limit execution to 60 fps on if display is 120 Hz
const fps = 60;
let previousTimestamp = -(1000 / fps);

function update(timestamp) {
    if (timestamp - previousTimestamp > 1000 / fps) {
        socket.emit('frame');
        previousTimestamp = timestamp;
    }
    if (navigator.getGamepads().length > 0) {
        updateGamepad();
    }
    window.requestAnimationFrame(update);
}


function updateGamepad() {
    const gp = navigator.getGamepads()[0];
    let new_key = false;
    // window.socket.emit("gamepad_axis", gp.axis) this is not needed

    if (pressed) {
        for (let i = 0; i < gp.buttons.length; i++) {
            if (pressed[i] !== gp.buttons[i].pressed) {
                pressed[i] = gp.buttons[i].pressed;
                new_key = true;
            }
        }
    } else {
        for (const button of gp.buttons) {
            pressed.push(button.pressed);
        }
        new_key = true;
    }

    // This should avoid socket.emit if no key has changed state
    // I haven't tested
    if (new_key) {
        socket.emit("gamepad_button", pressed);
    }
}
