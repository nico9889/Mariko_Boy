const pressed = [];


function update(timestamp) {
    window.requestAnimationFrame(update);
    socket.emit('frame');
    if (navigator.getGamepads().length > 0) {
        updateGamepad();
    }
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
