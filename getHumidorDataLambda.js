'use strict';

console.log('Loading function');

const doc = require('dynamodb-doc');

const dynamo = new doc.DynamoDB();

module.exports.get = (event, context, callback) => {
    //console.log('Received event:', JSON.stringify(event, null, 2));

    const done = (err, res) => callback(null, {
        statusCode: err ? '400' : '200',
        body: err ? err.message : JSON.stringify(res),
        headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    });

    if (event.httpMethod == 'GET') {
      dynamo.scan({ TableName: 'humidor' }, function(err, data) {
        if (err) {
          done(err, data);
        } else {
          data.Items.reverse()
          data.Items = data.Items.slice(1, 11);
          data.Items.forEach(function(element, index, array) {
            element.timestamp = element.timestamp * 1000;
          });
          done(err, data);
        }
      });
    } else {
      done(new Error(`Unsupported method "${event.httpMethod}"`));
    }
};
