# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time

USERNAME = "akki"
DEVICE_ID = "Tello-XXXX"

# callback function
def subscribe_callback(client,userdata,message):
	print("-----------------------------")
	print("Received data:")
	print(message.payload)
	print("from topic:")
	print(message.topic)
	print("-----------------------------")

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("tello_client")
myMQTTClient.configureEndpoint("a13ju54lmusok8-ats.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/etc/ssl/certs/ca-certificates.crt", "certs/priv.pem", "certs/cert.pem")
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