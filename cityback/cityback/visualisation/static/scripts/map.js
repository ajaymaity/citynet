/* eslint-disable max-len */
let previousOccupancy = [];
let mapLoaded = false;
let firstJson = undefined;
let map;
let deltaSlider = 21600;

/**
 * Update the mapbox map from json.
 * @param {json} geoStation
 */
function updateMap(geoStation) {
    console.log('updating map');
    if (mapLoaded) {
        let geoFeatures = geoStation['features'];
        for (let i = 0; i < geoFeatures.length; i++) {
            let geoProperty = geoFeatures[i]['properties'];
            if (i in previousOccupancy &&
                geoProperty['occupancy'] === previousOccupancy[i]) {
                geoProperty['occupancyChanged'] = 0;
            } else {
                geoProperty['occupancyChanged'] = 1;
                previousOccupancy[i] = geoProperty['occupancy'];
            }
        }
        // noinspection Annotator
        map.getSource('bikesource').setData(geoStation, {});
    } else {
        // keep the data for when the map is loaded
        firstJson = geoStation;
    }
}

/**
 * Add events fuctions on the time slider
 */
function setupSlider() {
    document.getElementById('slider').addEventListener(
        'change', function(event) {
            // noinspection Annotator
            let val = parseInt(event.target.value);
            if (val in dateTimeOfIndex) {
                let datetime = dateTimeOfIndex[val];
                // update text in the UI
                document.getElementById('active-hour').innerText = datetime;
                let el = document.getElementById('deltaS');
                let deltaS = el.options[el.selectedIndex].value;
                deltaSlider = deltaS;
                // update the map
                webSocket.send(JSON.stringify({
                    'type': 'getMapAtTime',
                    'dateTime': datetime,
                    'deltaS': deltaS}));
            }
        });
    document.getElementById('slider').addEventListener('input', function(e) {
        let value = parseInt(e.target.value);
        if (value in dateTimeOfIndex) {
            let datetime = dateTimeOfIndex[value];
            // update text in the UI
            document.getElementById('active-hour').innerText = datetime;
        }
    });
    document.getElementById('deltaS').addEventListener('change', function() {
        getDeltaDependentFunction();
    });
}

/**
 * Create the mapbox area with the key and input functions
 */
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

    let draw = new MapboxDraw({
        displayControlsDefault: false,
        controls: {
            polygon: true,
            trash: true,
        },
    });
    map.addControl(draw);


    map.on('draw.create', getPolygon);
    map.on('draw.delete', getPolygon);
    map.on('draw.update', getPolygon);

    /**
     * Handler when a polygon is selected, deleted or created
     * @param {mapObject} element
     */
    function getPolygon(element) {
        // let data = draw.getAll();
        let selectedPolygon = {};

        if ((element.type === 'draw.create' || element.type === 'draw.update')
            && element.features) {
            let dataPoint = element.features[0];

            dataPoint.paint = {
                'fill-color': '#088',
                'fill-opacity': 0.8,
            };

            selectedPolygon[dataPoint.id] = 'POLYGON(' +
                dataPoint.geometry.coordinates.map(function(ring) {
                    return '(' + ring.map(function(p) {
                        return p[0] + ' ' + p[1];
                    }).join(', ') + ')';
                }).join(', ') + ')';

            console.log(selectedPolygon);
            webSocket.send(JSON.stringify({
                'type': 'polygonData',
                'selectedPolygon': selectedPolygon,
                'deltaS': deltaSlider,
            }));
        } else if (element.type === 'draw.delete' && element.features) {
            // delete graph
        }
    }


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
        if (firstJson !== undefined) {
            updateMap(firstJson);
        }
    });
    setupWebSocket();
    setupSlider();


    map.on('click', 'bikes', function(e) {
        let coordinates = e.features[0].geometry.coordinates.slice();
        let description = ('Station No. ' + e.features[0].properties['station_number'] +
            '</br>' + e.features[0].properties['station_name']);

        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        webSocket.send(JSON.stringify({
                'type': 'stationSelect',
                'stationId': e.features[0].properties['station_number'],
                'deltaS': deltaSlider,
            }));

        new mapboxgl.Popup()
            .setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);
    });
}

window.addEventListener('load', initMap);
