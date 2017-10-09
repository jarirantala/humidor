# humidor
Read temperature and humidity from my cigar humidor using Ruuvitag sensor. Data is read by Raspberry Pi and published in AWS via their IoT service.

## Dependencies

### Ruuvitag

To collect the data from my humidor.

https://tag.ruuvi.com

### Raspberry Pi w/ bt and wi-fi

To read data from Ruuvitag and publish it into AWS IoT service.

https://www.raspberrypi.org/products/raspberry-pi-3-model-b/

TODO: add the scripts for Pi into repository.

### AWS cloud service

To store the data from humidor and publish it on a website.

Services in use: IoT, Lambda, DynamoDB, S3

https://aws.amazon.com

#### Serverless Framework

For AWS deployment.

https://serverless.com

##### Serverless Finch plugin

For AWS S3 static website deployment

https://www.npmjs.com/package/serverless-finch
