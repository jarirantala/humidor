# humidor
Read temperature and humidity from my cigar humidor using Ruuvitag sensor. Data is read by Raspberry Pi and published in AWS via their IoT service.

![Alt text](architecture.png?raw=true "Architecture")

## Dependencies

### Ruuvitag

To measure the data in my humidor.

https://tag.ruuvi.com

### Raspberry Pi w/ bt and wi-fi

To collect data from Ruuvitag and publish it into AWS IoT service.

https://www.raspberrypi.org/products/raspberry-pi-3-model-b/

TODO: add the scripts for Pi into repository.

### AWS cloud service

A serverless solution to subscribe to the data from Pi, save it into a dynamodb table, and publish it on an S3 website.

Services in use: IoT, Lambda, DynamoDB, S3

https://aws.amazon.com

#### Serverless Framework

For AWS deployment.

https://serverless.com

TODO: Add dynamodb table

##### Serverless Finch plugin

For AWS S3 static website deployment

https://www.npmjs.com/package/serverless-finch
