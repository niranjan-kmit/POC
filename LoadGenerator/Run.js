const http = require('http');
const WebSocket = require('ws')
var fs = require("fs");

//const {
//    WEB_SOCKET_URL,
//    REQUEST_TYPE,
//} = process.env;

var result = [];
var connections=[];
//const webSocketUrl = 'wss://taj0zjsvv5.execute-api.us-east-1.amazonaws.com/test/';
const webSocketUrl = 'ws://realtime-pushpin-b27e96fcf05cd2ba.elb.us-east-1.amazonaws.com/ws';

//const webSocketUrl = 'ws://localhost:7999/ws';
//const webSocketUrl = 'http://localhost:7999/stream?cname=hari'


const totalReq = parseInt(process.argv[2]);
const numofConnectionsPerSec = parseInt(process.argv[3]);
const executeTime = parseInt(process.argv[4]);

var intervalId = null;
var varCounter = 1;
var varName = function () {
    if (varCounter <= totalReq) {
        createConnectionOnTimer(numofConnectionsPerSec)
    } else {
        clearInterval(intervalId);
    }
};

intervalId = setInterval(varName, 1000);

function createConnectionOnTimer(numofConnectionsPerSec) {
    for (i = 0; i < numofConnectionsPerSec; i++) {
        createWebSocketConnection(webSocketUrl, varCounter, function (data) {
            //arr.push(data)
        });
		console.log("WebSocket Connection: " + varCounter);
        varCounter++;
    }
}

function createWebSocketConnection(webSocketUrl, varCounter, callback) {
    const connection = new WebSocket(webSocketUrl);
   
    connection.onopen = (evt) => {
		console.log("Opened" + varCounter);
//		connection.send('Hello');
//		connection.send('{"action":"onMessage","message":{"type":"pricing_req","conflationDelivery":"last","conflationType":"C-1","item":{"symbols":["DU211ZZ"],"fields":[]},"correlationId":"1","source":"PLATTS"}}');
    };
    connection.onerror = (error) => {
        try {
//			var errMessage = `ThreadId ${varCounter} WebSocket error: ${error.message}`
            console.log(error);
//			writeDataToFile(errMessage)
        }
        catch (error) {
 //           console.log(`ThreadId ${varCounter} WebSocket error: ${error.message}`);
        }
    };

	connection.onclose  = (evt) => {
	//	var closeMessage = `ThreadId ${varCounter} Closed: ${JSON.stringify(evt)}`;
        console.log(evt);
	//	writeDataToFile(closeMessage);
	}
	
    connection.onmessage = (e) => {
		var object = e.data;
//        result.push(JSON.stringify(object));
		var logMessage = `Thread ${varCounter} : Message ${JSON.stringify(object)}`;
     	console.log(logMessage);
		writeDataToFile(logMessage);
//     	return callback(JSON.stringify(object))
    };
}

function writeDataToFile(data) {
    fs.appendFile("report.txt", data + "\n", (err) => {
        if (err) console.log(err);
        // console.log("Successfully Written to File.");
    });
}
