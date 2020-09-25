const electron = require('electron');
const url = require('url');
const path = require('path');
const { execFile } = require('child_process');
const { spawn } = require('child_process');


global.appRoot = path.resolve(__dirname);

const { app, BrowserWindow, Menu, ipcMain} = electron;

//set a global window = mainwindow for navigation
global.mainWindow;
global.window = "mainWindow.html";

//no user has been logged in on startup
global.user = {name: null};

//on ready start a mainwindow using a browserwindow with a few settings- than load mainwindow.html in that browserwindow
app.on('ready', function(){
    
    mainWindow = new BrowserWindow({ show: false, frame: false,  backgroundColor: "#000000", width: 1200, height: 1920, fullscreen: true});
    //load HTML into window
    mainWindow.loadURL(url.format({
        pathname: path.join(__dirname, "./screens/mainWindow.html"),
        protocol:'file:',
        slashes: true,
    }));
    mainWindow.maximize();
    mainWindow.show();
    
});

// if the IPC commmand newwindow is triggered with the new screen name as argument, Change window
ipcMain.on('newwindow', function (e, new_window) {
    global.window = new_window;
    mainWindow.loadURL(url.format({
        pathname: path.join(__dirname, "./screens/"+new_window),
        protocol:'file:',
        slashes: true,
    }));
    //when a new window is loaded the "did-finish-load" commands fires up. 
    mainWindow.webContents.on('did-finish-load', () => {
        //mainWindow.webContents.send('test','This is a test');
    })
})

//if a user has been logged in, start hand gesture control 
ipcMain.on('login', function (e, user_name) {
    
    const ls = spawn('python3m',  ['./plugins/hand_gesture.py']);
    ls.stdout.on('data', (data) => {
            //main window is set by startup or by the IPC command "newwindow". Send this window the commannd "navigation" with the argument "left" or "right"
            if (data.includes("left")){
                console.log("left");
                can_hand = false;
                mainWindow.webContents.send("navigation", "left");
            } else if (data.includes("right")){
                console.log("right");
                can_hand = false;
                mainWindow.webContents.send("navigation", "right");
            }

    });
    //console log errors
    ls.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
    });

})

//close all windows on IPC close command

ipcMain.on('closeAllWindows', function (e, arg) {
    console.log("Closed by Q command");
    mainWindow.close();
})


const mainMenuTemplate = [
    {
    }
]