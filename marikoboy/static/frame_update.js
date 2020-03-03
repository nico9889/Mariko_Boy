function update(){
	updateGamepad();
	updateImage();				
	window.requestAnimationFrame(update);
}

function updateImage() {
	document.getElementById("image").src="/img.jpg?t=" + new Date().getTime(); // reload updated image without caching
}

function updateGamepad() {
	var gp = navigator.getGamepads()[0];
	// window.socket.emit("gamepad_axis", gp.axis) this is not needed
	var pressed = new Array(gp.buttons.lenght);
	for(i=0;i<gp.buttons.length;i++){
		pressed[i] = gp.buttons[i].pressed;
	}
	socket.emit("gamepad_button", pressed);
}
