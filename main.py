import network
import time
import ubinascii
import machine
import urequests
import utime
import random
import json
import urequests


url = "http://oepnweathermap.org/api"

headers = { "Content-Type": "application/json"
    }


MQTT_BROKER = "102.220.86.237" #"test.mosquitto.org" #"102.220.86.237" 
MQTT_CLIENT_ID= ubinascii.hexlify(machine.unique_id())
MQTT_PORT = 1883
UserName = "playerone"
User_PassWord = "challengeaccepted"
 
def connect_client():
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT,user="playerone",password= "challengeaccepted")
    #client.set_callback(mqtt_callback)
        client.connect()
    #client.subscribe(MQTT_TOPIC_SUBSCRIBE)
        print("Connected to MQTT broker")

        return client
    except Exception as e:
        print ("Error :", e)

def consume_message(Topic):
    try:
        print("Consume")
        client = connect_client()
        client.set_callback(get_response)
        client.subscribe(Topic)
           # client.connect()
        client.wait_msg()
        
    except Exception as e:
        print("Exception occured :", e)
    finally:
        client.disconnect()
#def publish_message(Topic,Payload):
    #try:
     #   client=connect_client()
     #   client.publish(Topic,Payload)
       
    #except Exception as e:
     #   print("Exception occured :", e)
    
def get_response (topic,msg):
    try:
        mqtt_directives = msg.decode("utf-8")
        print( mqtt_directives)           
    except Exception as e:
        print("Exception occured :", e)
   
last_publish_time = 0	
publish_interval = 10
topic = "icemachine/" + MQTT_CLIENT_ID.decode("uft-8") 
print(topic)

def initilize():
    APIKey = '6c4c8cd23f16a882b1d4f0b6b931dbe2'
    data = {}
    #response = urequests.post("http://api.openweathermap.org/data/2.5/weather?q=Benoni,ZAF&appid="+ APIKey+"&units=metric",json=data)
    #publishWeather(response.text)
    
#def publishWeather(payload):
 #   try:
        #topic = 'icemachine' + MQTT_CLIENT_ID.decode("utf-8") + '/weather'
        #client = connect_client()
        #client.publish(topic + "/weather",payload)
 #   except Exception as e:
 #       print("Exception occured :", e)
 #   finally:
        #client.disconnect()  
class iceCreamMachine(object):
    def __init__(self):
        self.id = MQTT_CLIENT_ID.decode("uft-8")
        self.drumTemp = random.randint(-6,45)
        self.resTemp = random.randint(-6,45)
        self.extTemp = random.randint(-6,45)
        self.fanStatus = True
        self.motorStatus = False
        self.motoSpeed = random.randint(0,100)
        
def buildData():
    machinevalues = iceCreamMachine()
    data = json.dumps(machinevalues.__dict__) 
    return data

initilize()
while True:
    current_time = utime.time()
    if current_time - last_publish_time >= publish_interval:
        data = buildData()
        print(data)
      #  publish_message(topic + "/post",data)
        #consume_message(topic +  "/get")
        last_publish_time = current_time
        
