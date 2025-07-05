document.onreadystatechange = (state) => {
	alert("Documento caricato correttamente");
	console.log("docuement state:", document.readyState);
	if (document.readyState === "complete") {
		window.requestAnimationFrame(update);
	}
}