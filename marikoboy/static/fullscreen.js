function fullscreen(){
    element = $('#container').get(0);
    if (element.requestFullscreen) {
      element.requestFullscreen();
    } else if (element.mozRequestFullScreen) {
      element.mozRequestFullScreen();
    } else if (element.webkitRequestFullscreen) {
      element.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
    } else if (element.msRequestFullscreen) {
      element.msRequestFullscreen();
    }    
}
