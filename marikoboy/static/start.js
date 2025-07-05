document.onreadystatechange = (state) => {
	console.log("docuement state:", document.readyState);
	if (document.readyState === "complete") {
		window.requestAnimationFrame(update);
	}
}