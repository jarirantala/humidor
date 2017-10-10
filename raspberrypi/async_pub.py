'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 * This file is modified by Jari Rantala
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
import argparse
from ruuvitag_sensor.ruuvitag import RuuviTag
from datetime import datetime, timedelta

# General message notification callback
def customOnMessage(message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


# Suback callback
def customSubackCallback(mid, data):
    print("Received SUBACK packet id: ")
    print(mid)
    print("Granted QoS: ")
    print(data)
    print("++++++++++++++\n\n")


# Puback callback
def customPubackCallback(mid):
    print("Received PUBACK packet id: ")
    print(mid)
    print("++++++++++++++\n\n")

parser = argparse.ArgumentParser()
host = "AWS IoT endpoint"
rootCAPath = "root_cert_path"
certificatePath = "cert_path"
privateKeyPath = "private_key_path"
useWebsocket = False
clientId = "id_defined_in_aws_iot"
topic = "topic_aws_iot_rule_is_listening_to"

if (not certificatePath or not privateKeyPath):
    parser.error("Missing credentials for authentication.")
    exit(2)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.onMessage = customOnMessage

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
# Note that we are not putting a message callback here. We are using the general message notification callback.
myAWSIoTMQTTClient.subscribeAsync(topic, 1, ackCallback=customSubackCallback)
myAWSIoTMQTTClient.subscribeAsync(topic, 1, ackCallback=customSubackCallback)
time.sleep(2)

mac = 'D7:CB:01:3A:C1:34'
sensor = RuuviTag(mac)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    data = sensor.update()

    tem = str(data['temperature'])
    hum = str(data['humidity'])
    now = datetime.now()
    exp = now + timedelta(hours = 3)
    expiration_date = str(int(exp.timestamp()))
    timestamp = str(int((now.timestamp()))
    msg = '{"timestamp": "' + timestamp + '", "expiration_date": "' + expiration_date + '", "humidity": "' + hum  + '", "temperature": "' + tem + '"$
    myAWSIoTMQTTClient.publishAsync(topic, msg, 1, ackCallback=customPubackCallback)
    loopCount += 1
    time.sleep(900)
