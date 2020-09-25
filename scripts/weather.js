var fs = require('fs');

//get the weather from the city - currently eindhoven but should be changeable later - and display it with correct icons to the main screen.
const userAction = async () => {
    var city = "eindhoven"
    //get the response from the api call
    const response = await fetch('http://openweathermap.org/data/2.5/weather?q='+city+'&appid=b6907d289e10d714a6e88b30761fae22');
    const myJson = await response.json(); //extract JSON from the http response
    var main = myJson.weather[0].main;
    var id = myJson.weather[0].id;
    var weather_icon = myJson.weather[0].icon;
    var description = myJson.weather[0].description;
    var temperature = myJson.main.temp;
    
    var icon_description = description.replace(" ", "_");

    //check if there is an icon with either id, description, weather_icon id
    //if there are none use the default icon from tha main folder
    //if there is no default icon, change icon to "unknown.svg" as protection for errors.
    var icon = "icons/"+main+"/"+id+".svg";

    if (checkImage(icon) == true){
        change_weather(icon, city, description, temperature);
    } else {
        icon = "icons/"+main+"/"+icon_description+".svg";
        if (checkImage(icon) == true){
            change_weather(icon, city, description, temperature);
        } else {
            icon = "icons/"+main+"/"+weather_icon+".svg";
            if (checkImage(icon) == true){
                change_weather(icon, city, description, temperature);
            }else{
                icon = "icons/"+main+"/default.svg";
                if (checkImage(icon) == true){
                    change_weather(icon, city, description, temperature);
                } else {
                    icon = "icons/unknown.svg";
                    change_weather(icon, city, description, temperature);
                }
            }
        }
    }
}

//function to check if the file (url) exists
function checkImage(url) {
    if (fs.existsSync(url)) { 
        return true
    } else {
        return false;
    }
}

//function to change the weather icon, temperature, description and city on the mainwindow.html
function change_weather(this_icon, city, description, temperature){
    document.getElementById("weather_icon").src = '../' + this_icon;
    document.getElementById("weather_temperature").innerHTML = temperature;
    document.getElementById("weather_description").innerHTML = description.capitalize();
    document.getElementById("weather_city").innerHTML = city.capitalize();
    
    //fade the weather icon, temperature, description and city in going from top to bottom
    document.getElementById("weer").classList.add('fadeInDown');
        
    
}

//function to give the city a capital first letter.
String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

//start script and refresh script every 10 seconds
userAction()  
setInterval(function(){
    userAction()  
},10000);
