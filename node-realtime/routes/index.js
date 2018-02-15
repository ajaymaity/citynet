var express = require('express');
var axios = require('axios');


var router = express.Router();

// Why AXIOS
// https://medium.com/@thejasonfile/fetch-vs-axios-js-for-making-http-requests-2b261cdd3af5

module.exports = io => {
	var localv = 100;
	const getApiAndEmit = async socket => {
	  try {
	    localv += 1;
	    console.log('tests ' + localv);
	    socket.emit('FromAPI', localv); // Emitting a new message. It will be consumed by the client
	  } catch (error) {
	    console.error('Error11:' + error);
	  }
	};
    
    let interval;

	io.on("connection", socket => {
	  console.log("New client connected");
	  if (interval) {
	    clearInterval(interval);
	  }
	  interval = setInterval(() => getApiAndEmit(socket), 1000);
	  socket.on("disconnect", () => {
	  	clearInterval(interval);
          console.log("Client disconnected");
	  });
	});

    return router;
}


