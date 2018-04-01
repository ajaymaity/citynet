/* eslint-disable max-len */
let previousOccupancy = [];
let mapLoaded = false;
let firstJson = undefined;
let map;
let draw;
let deltaSlider = 21600;
let iterators = new Set();
let stationsInChart = new Set();
let polygonLabelMap = {};
let requestInProgress = 0;
let lastGeoJson;

// requestInProgress.registerListener(function() {
//     if (requestInProgress === false) {
//         $('#loading').hide();
//     } else {
//         $('#loading').show();
//     }
// });


function showLoadingScreen() {
    requestInProgress += 1;
    $('#loading').show();
}

function hideLoadingScreen() {
    if (requestInProgress > 0) requestInProgress -= 1;
    if (requestInProgress === 0) $('#loading').hide();
}

/**
 * Update the mapbox map from json.
 * @param {json} geoStation
 */
function updateMap(geoStation) {
    console.log('updating map');
    if (mapLoaded) {
        let geoFeatures = geoStation['features'];
        console.log('geofeatures length: ' + geoFeatures.length);
        for (let i = 0; i < geoFeatures.length; i++) {
            geoFeatures[i].properties['charted'] = 0;
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
        if (!lastGeoJson) {
            lastGeoJson = geoStation;
            map.getSource('bikesourcefilter').setData(lastGeoJson);
        }
    } else {
        // keep the data for when the map is loaded
        firstJson = geoStation;
    }
}

function applyDeltaSliderUpdates() {
    removeAllDatasetsAndLabelsFromChart();
    showLoadingScreen();
    let type = 'draw.update';
    let allPolygons = draw.getAll();
    for (let elementId of stationsInChart) {
        let station = lastGeoJson.features.filter(function(d) {
            return d.properties['station_number'] === elementId;
        })[0];
        addStationToChart(elementId, station);
    }
    map.getSource('bikesourcefilter').setData(lastGeoJson);
    for (let polygon of allPolygons.features) {
        let features = [];
        features.push(polygon);
        getPolygon({
            'type': type,
            'features': features,
        });
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
                if (deltaSlider != deltaS) {
                    deltaSlider = deltaS;
                    applyDeltaSliderUpdates();
                }
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
 * Handler when a polygon is selected, deleted or created
 * @param {mapObject} element
 */
function getPolygon(element) {
    // let data = draw.getAll();
    let selectedPolygon = {};

    if ((element.type === 'draw.create' || element.type === 'draw.update')
        && element.features) {
        let dataPoint = element.features[0];

        if (element.type === 'draw.create') {
            let iterator = 1;
            while (iterators.has(iterator)) iterator += 1;
            polygonLabelMap[dataPoint.id] = 'Area ' + iterator;
            iterators.add(iterator);
        }

        if (element.type === 'draw.update') {
            removeDatasetFromChart(dataPoint.id);
            try {
                map.removeLayer(dataPoint.id);
                map.removeSource(dataPoint.id);
            } catch (e1) {}
        }

        dataPoint.paint = {
            'fill-color': '#088',
            'fill-opacity': 0.8,
        };

        selectedPolygon['id'] = dataPoint.id;
        selectedPolygon['polygon'] = 'POLYGON(' +
            dataPoint.geometry.coordinates.map(function(ring) {
                return '(' + ring.map(function(p) {
                    return p[0] + ' ' + p[1];
                }).join(', ') + ')';
            }).join(', ') + ')';

        let centroidPt = turf.centroid(dataPoint);
        centroidPt.properties.title = 'label';

        map.addSource(dataPoint.id, {
            'type': 'geojson',
            'data': centroidPt,
        });

        // Add the label style
        map.addLayer({
            'id': dataPoint.id,
            'type': 'symbol',
            'source': dataPoint.id,
            'layout': {
                'text-field': polygonLabelMap[dataPoint.id],
                'text-size': 50,
            },
            'paint': {
                'text-color': 'black',
            },
        });

        console.log(selectedPolygon);
        webSocket.send(JSON.stringify({
            'type': 'polygonData',
            'selectedPolygon': selectedPolygon,
            'deltaS': deltaSlider,
        }));
        showLoadingScreen();
    } else if (element.type === 'draw.delete' && element.features) {
        // delete graph
        let delIterator = Number(polygonLabelMap[element.features[0].id].match(/\d+/)[0]);
        iterators.delete(delIterator);
        delete polygonLabelMap[element.features[0].id];
        removeDatasetFromChart(element.features[0].id);
        try {
            map.removeLayer(element.features[0].id);
            map.removeSource(element.features[0].id);
        } catch (e1) {}
    }
}

function addStationToChart(elementId, station) {
    showLoadingScreen();
    station.properties['charted'] = 1;
    webSocket.send(JSON.stringify({
        'type': 'stationSelect',
        'stationId': elementId,
        'deltaS': deltaSlider,
    }));
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

    draw = new MapboxDraw({
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
                'circle-radius': [
                    'interpolate', ['linear'], ['zoom'],
                    12, 7,
                    14, 18,
                ],
                'circle-opacity': 1.0,
                'circle-stroke-width': [
                    'interpolate', ['linear'], ['zoom'],
                    12, 1,
                    14, 3,
                ],
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
        map.addSource('bikesourcefilter', {type: 'geojson', data: empty});
        map.addLayer({
            'id': 'stations-selected',
            'type': 'circle',
            'source': 'bikesourcefilter',
            'paint': {
                'circle-color': '#6e599f',
                'circle-radius': [
                    'interpolate', ['linear'], ['zoom'],
                    12, 7,
                    14, 18,
                ],
                'circle-stroke-width': [
                    'interpolate', ['linear'], ['zoom'],
                    12, 1,
                    14, 3,
                ],
                'circle-stroke-color': {
                    property: 'occupancyChanged',
                    type: 'exponential',
                    stops: [
                        [0, '#000000'],
                        [1, '#D00000'],
                    ],
                },
                'circle-opacity': {
                    property: 'charted',
                    type: 'exponential',
                    stops: [[0, 0], [1, 1]],
                },
            },
            // 'filter': ['in', 'FIPS', ''],
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
            '</br>' + e.features[0].properties['station_name'])
            +'</br> <button id = station_' + e.features[0].properties['station_number']
            + '> click to add/remove on chart </button>';

        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        new mapboxgl.Popup()
            .setLngLat(coordinates)
            .setHTML(description)
            .addTo(map);

        let btn = document.getElementById('station_' + e.features[0].properties['station_number']);
        btn.onclick = function(e1) {
            let elementId = e1.currentTarget.id.match(/\d+/)[0];
            let station = lastGeoJson.features.filter(function(d) {
                return d.properties['station_number'] === elementId;
            })[0];
            if (stationsInChart.has(elementId)) {
                stationsInChart.delete(elementId);
                removeDatasetFromChart(elementId);
                station.properties['charted'] = 0;
            } else {
                addStationToChart(elementId, station);
            }
            map.getSource('bikesourcefilter').setData(lastGeoJson);
        };
    });
}

window.addEventListener('load', initMap);
