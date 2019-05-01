# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import tello
from tello_alexa import TelloAlexa

USERNAME = "akki"
DEVICE_ID = "Tello-XXXX"

# callback function
def subscribe_callback(client,userdata,message):
	payload = json.loads((message.payload).decode("utf-8"))
	if payload['command'] == "checkroom":
		# command tello to look around
		print("inside checkroom") 
		telloController.checkForFaces()
	else:
		print("unsupported command")

# Init
drone = tello.Tello('', 8889)  
telloController = TelloAlexa(drone,"./img/")
myMQTTClient = AWSIoTMQTTClient("tello_client")
myMQTTClient.configureEndpoint("a13ju54lmusok8-ats.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials(	"certs/AmazonRootCA1.pem", 
									"certs/priv.pem", 
									"certs/cert2.pem")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

topic_name = "cmd/tello/"+USERNAME+"/"+DEVICE_ID
print(topic_name)

myMQTTClient.connect()
myMQTTClient.subscribe(topic_name,1,subscribe_callback)

while True:
	time.sleep(1)