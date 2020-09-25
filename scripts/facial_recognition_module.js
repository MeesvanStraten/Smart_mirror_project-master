var nodeConsole = require('console');
var myConsole = new nodeConsole.Console(process.stdout, process.stderr);
const { execFile } = require('child_process');
var remote = require('electron').remote;     
const {ipcRenderer} = require('electron')


//set counters for facial recognition
var unknown_counter = 0;
var known_name;
var known_counter = 0;

//function to start facial recognition

function start_facial() {
    myConsole.log("FACIAL HAS STARTED LOG THIS!");
    //start a python script - located at plugins/facial.py
    var SmartMirror_FaceRecognition = execFile('python3m', ['./plugins/facial.py'], (error, stdout, stderr) => {
        if (error) {
            throw error;
            myConsole.log(error);               
        }
    })
    
    //wait for the pythonscript to flush a stdout with data
    SmartMirror_FaceRecognition.stdout.on('data',function(data){
        myConsole.log(data);
        //create the variable face_name with the new data & parse it to json for easier editing in javascript
        var face_name = data.toString('utf8');
        face_name = face_name.replace(/'/g, '"');
        face_name = JSON.parse(face_name);
            
        
        // Check if face is unknown or not. it can try 5 times if unknown and 2 times if known. We do this to ensure the user is actually that user.
        if (face_name[0].includes("Unknown")){
            unknown_counter++;
            if (unknown_counter > 4){
                unknown_counter = 0;
                SmartMirror_FaceRecognition.kill();  
                document.getElementById("name").innerHTML = "unknown person";
                document.getElementById('save_new').disabled = false;
                document.getElementById("bericht").classList.add('fadeInUp');
                document.getElementById("new_user_box").classList.add('fadeInUp');
            }
            
        } else {
            //if faces is known, show the user a welcome message and set global.user to face name
            if (face_name[0] == known_name){
                known_counter++
                if (known_counter > 2){
                    known_counter = 0;
                    SmartMirror_FaceRecognition.kill();  
                    document.getElementById("name").innerHTML = face_name[0];
                    document.getElementById("bericht").classList.add('fadeInUp');
                    remote.getGlobal('user').name = face_name[0];
                    setTimeout(function(){
                        document.getElementById("welkomtekst").classList.add('fadeOut');
                        document.getElementById("welkomtekst").classList.add('slow');
                        setTimeout(function(){
                            document.getElementById("mainNavigator").classList.remove('hidden');
                            document.getElementById("mainNavigator").classList.add('fadeIn');
                            document.getElementById("mainNavigator").classList.add('slow');
                        }, 2000)
                    }, 2000)
                }
            } else {
                setTimeout(function(){
                    known_name = face_name[0];
                    ipcRenderer.send('login', face_name[0])
                    known_counter = 0;
                }, 500)
            }
        }
    });
}

//this function is to save a new face. This will later be changed so that the new user will be saved in electron, and not a txt file.
function save_new_user() {
    var newName = document.getElementById("new_username").value;
    if (newName != ("")){
        var newFacePython = execFile('python3m', ['./plugins/new_face.py', newName], (error, stdout, stderr) => {
            if (error) {
                throw error;
            }
            myConsole.log(stdout);
        })
        newFacePython.stdout.on('data',function(data){
            if (data.includes("done")){
                document.getElementById('save_new').disabled = true;
                start_facial();
            } else if(data.includes("No_face")){
                console.log('Opnieuw proberen');
                //alert("Ga voor de spiegel staan, over 5 seconden proberen we het opnieuw");
                setTimeout(function () {
                        save_new_user();
                }, 2500);
            }
        })
    } else {
        alert("Vul iets in als naam");
    }
}

//if the page is reloaded, check if a user is logged in. If not start the face_recognition function. Else show navigation icons
if (remote.getGlobal('user').name == null){
    start_facial()
    // ipcRenderer.send('login', 'v')
} else {
    document.getElementById("welkomtekst").classList.add('hidden');
    document.getElementById("mainNavigator").classList.remove('hidden');
    document.getElementById("mainNavigator").classList.add('fadeIn');
    document.getElementById("bericht").classList.add('fadeIn');
   
}
