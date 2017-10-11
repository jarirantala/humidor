# humidor
Read temperature and humidity from my cigar humidor using Ruuvitag sensor. Data is read by Raspberry Pi and published in AWS via their IoT service.

![Alt text](images/architecture.png?raw=true "Architecture")

## Dependencies

### Ruuvitag

To measure the data in my humidor.

https://tag.ruuvi.com

### Raspberry Pi w/ bt and wi-fi

To collect data from Ruuvitag and publish it into AWS IoT service.

https://www.raspberrypi.org/products/raspberry-pi-3-model-b/

Usage: run the python3 script in raspberrypi-folder in your raspberry to collect sensor data. Preferably with *nohup python3 async_pub.py &* or as a service.

Requires https://github.com/aws/aws-iot-device-sdk-python and https://github.com/ttu/ruuvitag-sensor

### AWS cloud service

A serverless solution to subscribe to the data from Pi, save it into a dynamodb table using an IoT rule, and publish it on an S3 website.

Services in use: [IoT](https://aws.amazon.com/iot/), [Lambda](https://aws.amazon.com/lambda/), [DynamoDB](https://aws.amazon.com/dynamodb/), [S3](https://aws.amazon.com/s3/)

https://aws.amazon.com

#### Serverless Framework

For AWS deployment.

Usage:
- *serverless deploy* to deploy the backend application w/ database
- *serverless client deploy* to deploy static files to S3
- *serverless deploy function -f humidor* to deploy only the lambda function if you don't want to erase your dynamo table

https://serverless.com

TODO: Add IoT rule and TTL to dynamo table

##### Serverless Finch plugin

For AWS S3 static website deployment

https://www.npmjs.com/package/serverless-finch

#### Morris.js

A very simple js chart library. Requires also jquery.

http://morrisjs.github.io/morris.js/index.html

## Screenshot

![Alt text](images/screenshot.png?raw=true "Screenshot" | width=400)
