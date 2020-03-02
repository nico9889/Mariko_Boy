$(document).ready(function() {			
	$(window).on("gamepadconnected", function() {
		hasGP = true;			
	var req = new XMLHttpRequest();
		req.open('POST', '/streaming/', true);
		req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
		req.send("key=INIT");
		window.requestAnimationFrame(update);
	});

});
