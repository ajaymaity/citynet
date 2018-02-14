// import { SocketIO, Server } from 'mock-socket';

const mockServerA = require('mock-socket').Server;
const socketIO = require('mock-socket').SocketIO;

const index = require('../routes/index');

describe('client tests', () => {
	it('client connects', () => {
		const mockServer = new mockServerA('http://localhost:8080');
	    mockServer.on('connection', server => {
	      mockServer.emit('chat-message', 'test message 1');
	      mockServer.emit('chat-message', 'test message 2');
	    });

	    /*
	      This step is very important! It tells our chat app to use the mocked
	      websocket object instead of the native one. The great thing
	      about this is that our actual code did not need to change and
	      thus is agnostic to how we test it.
	    */
	    // window.io = SocketIO;

	    let sock = index(new socketIO());

	    setTimeout(() => {
	      let numConnectedClients = sock.numConnectedClients;
	      assert.equal(numConnectedClients, 1, 'one client connected');
	      mockServer.stop(done);
	    }, 100);


	})
});