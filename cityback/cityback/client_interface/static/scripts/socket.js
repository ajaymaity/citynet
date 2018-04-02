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
    let rtMode;

    // Check if in rtMode
    let slider = document.getElementById('slider');
    let selector = document.getElementById('deltaS');
    if (slider !== 'undefined' && slider.value === slider.max &&
        selector !== 'undefined' && getCurrentDelta() === '60') {
        document.getElementById('rt_updates').innerText = 'on';
        document.getElementById('rt_updates').style.fontWeight = 'bold';
        rtMode = true;
    } else {
        document.getElementById('rt_updates').innerText = 'off';
        document.getElementById('rt_updates').style.fontWeight = 'normal';
        rtMode = false;
    }

    // update real-time stations
    if (rtMode && 'rtstations' in svals) {
        updateMap(svals.rtstations, rtMode);
        let slider = document.getElementById('slider');
        slider.min = 0;
        slider.max = svals.timerange.nbIntervals - 1;
        slider.value = slider.max;
        dateTimeOfIndex = svals.timerange.dateTimeOfIndex;
        slider.dispatchEvent(new Event('input'));
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
                updateMap(svals.value, rtMode);
                break;
            case 'chart':
                console.log('Received Chart data!');
                replaceChart(svals.labels, svals.occupancy,
                    svals.selectionType, svals.selectionId,
                    svals.time_delta_s);
                break;
            case 'multichart':
                console.log('Received multi Chart data!');
                for (let i=0; i < svals.selectionsId.length; i++) {
                    replaceChart(svals.labels, svals.occupancy[i],
                        svals.selectionType, svals.selectionsId[i],
                        svals.time_delta_s);
                }
                break;
        }
    }
    hideLoadingScreen();
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
    webSocket = new WebSocket(
        prefix + '://' + location.host + '/ws/rtStations');
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

/* exported getChartData */
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
    // getChartData();
}

/**
 * Handler for socket connection opened, updates all delta dependent values
 */
function onOpen() {
    console.log('Connected to webSocket!');
    getDeltaDependentFunction();
}

/* exported requestForecast */
/**
 * Request for the chart forecast data
 * @param {String} startTime
 * @param {int} length
 * @param {Array} stations
 */
function requestForecast(startTime, length, stations) {
    webSocket.send(JSON.stringify({
        type: 'getForecast',
        start: startTime,
        length: length,
        stations: stations,
        }
    ));
}
