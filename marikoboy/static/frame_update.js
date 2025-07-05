let pressed = [];


function update() {
    updateGamepad();
    socket.emit('frame');

    window.requestAnimationFrame(update);
}


function updateGamepad() {
    let gp = navigator.getGamepads()[0];
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
        for (let i = 0; i < gp.buttons.length; i++) {
            pressed[i] = gp.buttons[i].pressed;
        }
        new_key = true;
    }

    // This should avoid socket.emit if no key has changed state
    // I haven't tested
    if (new_key) {
        socket.emit("gamepad_button", pressed);
    }
}
