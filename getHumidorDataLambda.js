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

    function getFormattedDate(datetime) {
        var month = datetime.getMonth() + 1;
        var day = datetime.getDate();
        var year = datetime.getFullYear();
        return day + "." + month;
    }

    function getFormattedTime(datetime) {
        var hours = datetime.getUTCHours().toString().length == 1 ? '0' + datetime.getUTCHours() : datetime.getUTCHours();
        var minutes = datetime.getMinutes().toString().length == 1 ? '0' + datetime.getMinutes() : datetime.getMinutes();
        var seconds = datetime.getSeconds().toString().length == 1 ? '0' + datetime.getSeconds() : datetime.getSeconds();
        return hours + ":" + minutes + ":" + seconds;
    }

    function getFormattedDatetime(datetime) {
        return getFormattedDate(datetime) + " " + getFormattedTime(datetime);
    }

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
