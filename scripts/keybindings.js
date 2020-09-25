var electron = require("electron");
var ipc = electron.ipcRenderer;

document.addEventListener('keydown', function(e) {
    //q key
    if (e.keyCode == 113 || e.keyCode == 81){
        e.keypress = '1';
        ipc.send('closeAllWindows', 'now');
    }
    //left arrow key
    if (e.keyCode == 37){
        e.keypress = '1';
        left();
    }
    //right arrow key
    if (e.keyCode == 39){
        e.keypress = '1';
        right();
    }
});