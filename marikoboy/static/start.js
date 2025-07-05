document.onreadystatechange = (state) => {
	if (document.readyState === "complete") {
		window.ongamepadconnected = (event) => {
			window.requestAnimationFrame(update);
		}
	}
}