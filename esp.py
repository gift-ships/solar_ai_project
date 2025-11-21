import network
#import time
from umqtt.simple import MQTTClient
import ubinascii
import machine
import urequests
import utime
import random
import json


url = "http://oepnweathermap.org/api"
headers = { "Content-Type": "application/json"
    }
wf_ssid = "VC-1053-8861"
wf_pass = "0fa8bdc688"

MQTT_BROKER = "test.mosquitto.org" #"102.220.86.237" 
MQTT_CLIENT_ID= ubinascii.hexlify(machine.unique_id())
MQTT_PORT = 1883
UserName = "playerone"
User_PassWord = "challengeaccepted"
 
def connect_to_wifi(ssid,password):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    if not sta_if.isconnected():
        print("Connect")
        sta_if.connect(ssid,password)
        while not sta_if.isconnected():
            time.sleep(1)
            
    print("connected")
    print("IP Address:",sta_if.ifconfig()[0])
def connect_client():
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)#,user="playerone",password= "challengeaccepted")
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
def publish_message(Topic,Payload):
    try:
        client=connect_client()
        client.publish(Topic,Payload)
       
    except Exception as e:
        print("Exception occured :", e)
    finally:
        client.disconnect()
    
def get_response (topic,msg):
    try:
        mqtt_directives = msg.decode("utf-8")
        print( mqtt_directives)           
    except Exception as e:
        print("Exception occured :", e)
    #finally:
     #   client.disconnect()
last_publish_time = 0	
publish_interval = 10
topic = "icemachine/" + MQTT_CLIENT_ID.decode("uft-8") 
print(topic)

def initilize():
    connect_to_wifi(wf_ssid,wf_pass)

class iceCreamMachine(object):
    def __init__(self):
        self.drumtemp = random.randint(-6,45)
        self.tankTemp = random.randint(-6,45)
        self.extTemp = random.randint(-6,45)
        #self.timestamp = RTC.init(datetime)

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
        publish_message(topic + "/post",data)
        #consume_message(topic +  "/get")
        last_publish_time = current_time
        print (MQTT_CLIENT_ID.decode("utf-8"))
        
#if __name__ == "__main__":
#run()