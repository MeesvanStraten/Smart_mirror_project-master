import Adafruit_DHT
import json
import sys 
import time

# we use sensor dht22
sensor = Adafruit_DHT.DHT22
# Set a wrong variable, so can refresh if it goes wrong to many times
hum_times_wrong = 0
temp_times_wrong = 0

# Set a check variable, so we can get the best out of 5
um_times_checked = 0
temp_times_checked = 0

# Last hum and temp to check
last_temp = 0
last_hum = 0

# all tempst and hums
all_temp = 0
all_hump = 0
# first startup var
first_check = True

# connected to GPIO pin 23 on the raspberry pi. (16)
pin = 23

# Collect data in a list
temp_list = []
hum_list = []

# while loop so it returns the temperature everytime
while True:
    # Create data object to send
    data = {}
    
    # Read sensor data
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if first_check is True:
        last_temp = temperature
        last_hum = humidity
        first_check = False
    
    if first_check is False:
        if temperature < (last_temp+2) and temperature > (last_temp-2) and humidity < (last_hum+2) and humidity > (last_hum-2):
            # print("Temperature seems fine?")
            last_temp = temperature
            temp_list.append(temperature)
            # print("humidity seems fine?")
            last_hum = humidity
            hum_list.append(humidity)
        else:
            # print("Temperature or Humidity IS FUCKED ")
            temp_times_wrong = temp_times_wrong + 1
            if temp_times_wrong > 4:
                # print("something fucked up")
                temp_times_wrong = 0
                last_temp = temperature
                last_hum = humidity

        if len(hum_list) > 5 and len(temp_list) > 5:
            for x in hum_list:
                all_hump = all_hump + x
            for x in temp_list:
                all_temp = all_temp + x
            
            data['temperature'] = round(all_temp/len(temp_list), 1)
            data['humidity'] = round(all_hump/len(hum_list), 1)

            json_data = json.dumps(data)
            print(json_data)
            sys.stdout.flush()

            all_temp = 0
            all_hump = 0
