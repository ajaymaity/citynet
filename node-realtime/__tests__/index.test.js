'use strict'

var expect = require('chai').expect;  
var io     = require('socket.io-client');

var app = require('../bin/www');

var socketUrl = 'http://localhost:3000';

var options = {  
  transports: ['websocket'],
  'force new connection': true
};

describe('Sockets', () => {
  let client1
  it('connect', function(done) {
    client1 = io.connect(socketUrl, options);
      client1.on('FromAPI', function(msg) {
        console.log(msg);
        expect(msg).to.equal(101);
        client1.disconnect();
        done();
      })
  })
})