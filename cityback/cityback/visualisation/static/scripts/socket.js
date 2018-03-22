var date_Time_Of_Index = [];
function onMessage(evt) {
    console.log('data_received');
    let svals = JSON.parse(evt.data);

    if ("stations" in svals) {
        updateMap(svals.stations);
    }
    if("type" in svals){
        // console.log('data=' + JSON.stringify(svals))
        switch (svals.type){
            case "timeRange":
                slider = document.getElementById('slider');
                slider.min = 0;
                slider.max = svals.nbIntervals - 1;
                slider.value = slider.max;
                date_Time_Of_Index = svals.dateTimeOfIndex;
                var event = new Event('change');
                slider.dispatchEvent(event);
                break;
            case "mapAtTime":
                console.log('Updating data...');
                console.log(svals.value);
                updateMap(svals.value);
                break;
            case "chart":
                console.log('Received Chart data!')
                addChart(svals.labels, svals.occupancy, svals.time_delta_s)
                break;
        }
    }
}

function setupWebSocket() {
    if (window.location.protocol != 'https:') {
        prefix = 'ws';
    } else {
        prefix = 'wss';
    }
    websocket = new WebSocket(prefix + '://'  + location.host + '/ws/rtStations');
    websocket.onopen = function(evt) {
        onOpen(evt);};
    websocket.onmessage = function(evt) {
        onMessage(evt);};
}

function getTimeRange(){
    var e = document.getElementById('delta_s')
    delta_s = e.options[e.selectedIndex].value
    websocket.send(JSON.stringify({
        type: "getTimeRange",
        delta_s: delta_s}
    ));
}

function onOpen(evt) {
    console.log('Connected to websocket!')
    getTimeRange()

}
