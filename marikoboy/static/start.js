$(document).ready(function() {			
	$(window).on("gamepadconnected", function() {
		window.requestAnimationFrame(update);
	});

});
