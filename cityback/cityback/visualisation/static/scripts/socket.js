/**
 * Handle the socket connection to the server
 */

/* exported dateTimeOfIndex */
let dateTimeOfIndex = [];

/**
 * Handler when receiving Socket messages
 * @param {MessageEvent} evt
 */
function onMessage(evt) {
    console.log('data_received');
    let svals = JSON.parse(evt.data);

    if ('stations' in svals) {
        updateMap(svals.stations);
    }
    if ('type' in svals) {
        // console.log('data=' + JSON.stringify(svals))
        switch (svals.type) {
            case 'timeRange':
                let slider = document.getElementById('slider');
                slider.min = 0;
                slider.max = svals.nbIntervals - 1;
                slider.value = slider.max;
                dateTimeOfIndex = svals.dateTimeOfIndex;
                slider.dispatchEvent(new Event('change'));
                break;
            case 'mapAtTime':
                console.log('Updating data...');
                console.log(svals.value);
                updateMap(svals.value);
                break;
            case 'chart':
                console.log('Received Chart data!');
                replaceChart(svals.labels, svals.occupancy, svals.time_delta_s);
                break;
        }
    }
}

/* exported webSocket */
// eslint-disable-next-line
var webSocket;

/* exported setupWebSocket */
/**
 * Initialise the webSocket connection
 */
function setupWebSocket() {
    let prefix;
    if (window.location.protocol !== 'https:') {
        prefix = 'ws';
    } else {
        prefix = 'wss';
    }
    webSocket = new WebSocket(prefix + '://' + location.host + '/ws/rtStations');
    webSocket.onopen = function(event) {
        onOpen();
};
    webSocket.onmessage = function(event) {
        onMessage(event);
};
}

/* exported getCurrentDelta */
/**
 * Get the current value of the deta_s select
 * @return {String}
 */
function getCurrentDelta() {
    let e = document.getElementById('deltaS');
    return e.options[e.selectedIndex].value;
}

/**
 * Request for timeRange on the socket
 */
function getTimeRange() {
    webSocket.send(JSON.stringify({
        type: 'getTimeRange',
        deltaS: getCurrentDelta()}
    ));
}

/**
 * Request for the chart values for the current time delta
 */
function getChartData() {
    webSocket.send(JSON.stringify({
        type: 'getChartWithDelta',
        deltaS: getCurrentDelta()}
    ));
}

/**
 * Request update for all elements dependent on the timeDelta value
 */
function getDeltaDependentFunction() {
    getTimeRange();
    getChartData();
}

/**
 * Handler for socket connection opened, updates all delta dependent values
 */
function onOpen() {
    console.log('Connected to webSocket!');
    getDeltaDependentFunction();
}
