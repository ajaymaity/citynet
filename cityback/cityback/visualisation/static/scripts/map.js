var previousOccuapancy = [];
var mapLoaded = false;
var firstJson = undefined;
var debug = false;
var map;


function updateMap(geoStation) {
    console.log("updating map")
    if (mapLoaded) {
        geoFeatures = geoStation['features'];
        for (let i = 0; i < geoFeatures.length; i++) {
            let geoProperty = geoFeatures[i]['properties'];
            if (i in previousOccuapancy &&
                geoProperty['occupancy'] == previousOccuapancy[i]) {
                geoProperty['occupancyChanged'] = 0;
            } else {
                geoProperty['occupancyChanged'] = 1;
                previousOccuapancy[i] = geoProperty['occupancy'];
            }
        }
        map.getSource('bikesource').setData(geoStation);
    }else{
        // keep the data for when the map is loaded
        firstJson = geoStation
    }
}


function pressButton() {
    debug = !debug;
    document.getElementById('dbg').innerHTML = debug;
}


function setupSlider() {
    document.getElementById('slider').addEventListener('change', function(e) {
        var value = parseInt(e.target.value);
        if(value in date_Time_Of_Index){
            datetime = date_Time_Of_Index[value]
            // update text in the UI
            document.getElementById('active-hour').innerText = datetime;
            var time_option = document.getElementById("time_delta");
            var time_delta = 60;
            // update the map
            websocket.send(JSON.stringify({
                type: "getMapAtTime", dateTime: datetime, timeDelta: time_delta}));
        }

    });
    document.getElementById('slider').addEventListener('input', function(e) {
        var value = parseInt(e.target.value);
        if(value in date_Time_Of_Index){
            datetime = date_Time_Of_Index[value]
            // update text in the UI
            document.getElementById('active-hour').innerText = datetime;
        }
    });
}

function initMap() {
// create mapbox object
    mapboxgl.accessToken = 'pk.eyJ1IjoiYXNlcHJvamVjdGdyb3VwMTEiLCJhIjoiY2pkdWE2dHRuMTVmODMzbGxzY3htNzVmZCJ9.rp6HgWPAmVtqsQ9pOR4PdA';
    map = new mapboxgl.Map({
        container: 'map', // container id
        style: 'mapbox://styles/aseprojectgroup11/cjdyqc4ce377n2sqij5ark9hb', // stylesheet location
        center: [-6.264, 53.346], // starting position [lng, lat]
        zoom: 13.25, // starting zoom
    });
// Add zoom and rotation controls to the map.
    map.addControl(new mapboxgl.NavigationControl());

// dict to store stations previous occupancy
    map.on('load', function() {
        let empty = {type: 'FeatureCollection', features: []};
        map.addSource('bikesource', {type: 'geojson', data: empty});
        map.addLayer({
            'id': 'bikes',
            'type': 'circle',
            'source': 'bikesource',
            'paint': {
                'circle-color':
                    {property: 'occupancy',
                        type: 'exponential',
                        stops: [[0, '#ffffff'],
                            [1, '#ccddff'],
                            [99, '#006bc0'],
                            [100, '#777777']]},
                'circle-radius': {
                    property: 'vacancy',
                    type: 'exponential',
                    stops: [[0, 15],
                        [100, 15]]},
                'circle-opacity': 1.0,
                'circle-stroke-width': {
                    property: 'occupancyChanged',
                    type: 'exponential',
                    stops: [
                        [0, 2],
                        [1, 3],
                    ],
                },
                'circle-stroke-color': {
                    property: 'occupancyChanged',
                    type: 'exponential',
                    stops: [
                        [0, '#000000'],
                        [1, '#D00000'],
                    ],
                },
            },
        });
        mapLoaded = true;
        if (firstJson != undefined) {
            updateMap(firstJson);
        }
    });
    setupWebSocket();
    setupSlider();
}

window.addEventListener('load', initMap);
