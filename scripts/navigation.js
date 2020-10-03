
var electron = require("electron");
var ipc = electron.ipcRenderer;
var remote = require('electron').remote;  

//if the command "navigation" is fired up with an argument, start function left or right
ipc.on("navigation", function(e, arg) {
    if (arg == "left"){
        left();
    }
    if (arg == "right"){
        right();
    }
});




var new_window;

//this is for testing purpose with a mouse. In the end product the user has no mouse so this click function can never be fired up.
document.getElementById('hidden_button_left').onclick = function() {left();};
document.getElementById('hidden_button_right').onclick = function() {right();};

//function left is to navigate the screen to left. If the screen is the last left screen it won't navigate left.
function left() {
    if (remote.getGlobal('window') == "mainWindow.html"){
        new_window = 'settingsWindow.html'
    } else if (remote.getGlobal('window') == "newsWindow.html"){
        new_window = 'mainWindow.html'
    } else if (remote.getGlobal('window') == "trainWindow.html"){
        new_window = 'newsWindow.html'
    } else if (remote.getGlobal('window') == "appWindow.html"){
        new_window = 'trainWindow.html'
    }
    if (new_window != null){
        //fade all elements out for a "smooth" transition
        document.getElementById('content').classList.add('fadeOutRight');
        document.getElementById('topIcon').classList.add('fadeOut');
        //after the function is done, wait one second for all animations and send the main javascript the new window name.
        setTimeout(function(){ 
            ipc.send('newwindow', new_window)
        }, 1000);
    }
}

//function right is to navigate the screen to right. If the screen is the last right screen it won't navigate right.
function right() {
    if (remote.getGlobal('window') == "settingsWindow.html"){
        new_window = 'mainWindow.html';
    } else if (remote.getGlobal('window') == "mainWindow.html"){
        new_window = 'newsWindow.html';
    } else if (remote.getGlobal('window') == "newsWindow.html"){
        new_window = 'trainWindow.html';
    } else if (remote.getGlobal('window') == "trainWindow.html"){
        new_window = 'appWindow.html';
    } else if (remote.getGlobal('window') == "appWindow.html"){
        new_window = null;
    }

    if (new_window != null){
        //fade all elements out for a "smooth" transition
        document.getElementById('content').classList.add('fadeOutLeft');
        document.getElementById('topIcon').classList.add('fadeOut');
        //after the function is done, wait one second for all animations and send the main javascript the new window name.
        setTimeout(function(){ 
            ipc.send('newwindow', new_window)
        }, 1000);
    }
}