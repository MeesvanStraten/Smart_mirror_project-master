
var data_received = false;
//read temperature function to get the temperature from the temperature sensor of the room
function read_temperature() {
    document.getElementById("huis_temp").innerHTML = "testx";
    var smartmirror_temp = execFile('python3m', ['./plugins/temperature.py'], (error, stdout, stderr) => {
        if (error) {
            throw error;
            myConsole.log(error);               
        }
    })
    
    //wait for the pythonscript to flush a stdout with data
    smartmirror_temp.stdout.on('data',function(data){
            if (data_received == false){
                document.getElementById("huis-temp-hum").classList.remove('hidden');
                document.getElementById("huis-temp-hum").classList.add('fadeIn');
                document.getElementById("huis-temp-hum").classList.add('slow');
                data_received = true;
            }

            var temp_hum = data;
            
            temp_hum = JSON.parse(temp_hum);

            document.getElementById("huis_temp").innerHTML = temp_hum["temperature"];
            document.getElementById("huis_hum").innerHTML = temp_hum["humidity"];

            // Check if face is unknown or not. it can try 5 times if unknown and 2 times if known. We do this to ensure the user is actually that user.
        
        
        });
}

read_temperature()
