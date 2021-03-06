
let MONTHS = ['January', 'February', 'March', 'April', 'May',
    'June', 'July', 'August', 'September', 'October', 'November', 'December'];

window.chartColors = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)',
};

/**
 * Generate a random number
 * @return {number}
 */
function randomValue() {
    return Math.round(Math.random() * 200 - 100);
}

let config = {
    type: 'line',
    data: {
        labels: [],
        datasets: [],
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: '6-hour average station occupancy',
        },
        showTooltips: false,
        hover: false,
        animation: {
            duration: 0,
        },
        scales: {
            xAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Time',
                },
            }],
            yAxes: [{
                display: true,
                scaleLabel: {
                    display: true,
                    labelString: 'Occupancy',
                },
            }],
        },
    },
};


window.onload = function() {
    let ctx = document.getElementById('canvas').getContext('2d');
    window.myLine = new Chart(ctx, config);
};


let colorNames = Object.keys(window.chartColors);


/* exported replaceChart */
/**
 * Draw a new graph, removing the previous one
 * @param {Array} labels
 * @param {Array} occupancy
 * @param {String} selectionType
 * @param {int} selectionId
 * @param {int} timeDeltaS
 */
function replaceChart(labels, occupancy, selectionType, selectionId,
                      timeDeltaS) {
    // get new color in list
    if (!selectionType) {
        return;
    }
    let colorName = colorNames[config.data.datasets.length % colorNames.length];
    let newColor = window.chartColors[colorName];
    let minutes = timeDeltaS / 60;
    let hours = minutes / 60;
    let timeStr;
    if (hours >= 1) {
        timeStr = hours + '-hour';
    } else {
        timeStr = minutes + '-minute';
    }

    let label;
    if (selectionType === 'station') {
        stationsInChart.add(String(selectionId));
        label = 'Station ' + selectionId;
    } else if (selectionType === 'polygon') {
        label = polygonLabelMap[selectionId];
    } else if (selectionType === 'forecast') {
        label = 'Forecast ' + selectionId;
    }
    let newDataset = {
        id: selectionId,
        label: label,
        backgroundColor: newColor,
        borderColor: newColor,
        pointRadius: 1,
        data: [],
        fill: false,
    };
    config.options.title.text = (`${timeStr} average station occupancy`);
    console.log('drawing chart with data:');

    let extraData = [];
    if (config.data.labels.length === 0 ) {
        for (let index = 0; index < labels.length; ++index) {
            config.data.labels.push(labels[index]);
        }
    } else if (config.data.labels[0] !== labels[0]) {
        let index;
        for (index = 0; index < config.data.labels.length; ++index) {
            if (config.data.labels[index] === labels[0]) {
               break;
            } else {
                extraData.push(null);
            }
        }
        for (let idx2 = 0; idx2 < labels.length; ++idx2) {
            if (idx2 + index >= config.data.labels.length) {
                config.data.labels.push(labels[idx2]);
            }
        }
    }
    for (let index = 0; index < extraData.length; ++index) {
        newDataset.data.push(extraData[index]);
    }

    for (let index = 0; index < occupancy.length; ++index) {
        newDataset.data.push(occupancy[index]);
    }

    config.data.datasets.push(newDataset);
    window.myLine.update();
}

/* exported removeDatasetFromChart */
/**
 * Remove a specific dataset from the chart.
 * @param {int} selectionId
 */
function removeDatasetFromChart(selectionId) {
    let removalIndex = config.data.datasets.indexOf(
        config.data.datasets.filter(
            function(dataObject) {
                return dataObject.id == selectionId; // force coercion
    })[0]);
    if (removalIndex >= 0) {
        config.data.datasets.splice(removalIndex, 1);
        window.myLine.update();
    }

    if (config.data.datasets.length === 0) {
        while (config.data.labels.length) {
            config.data.labels.pop();
        }
    }
}

/* exported removeAllDatasetsAndLabelsFromChart */
/**
 * Remove all the datasets and labels from the chart.
 */
function removeAllDatasetsAndLabelsFromChart() {
    while (config.data.datasets.length) {
        config.data.datasets.pop();
    }

    while (config.data.labels.length) {
        config.data.labels.pop();
    }
}


/* exported getForecastData */
/**
 * Ask for forecast data
 */
function getForecastData() {
   console.log('starting forecast');
    let slider = document.getElementById('slider');
    if (slider === 'undefined') return;
    let pos = slider.value;
    if (! pos in dateTimeOfIndex) return;
    let startTime = dateTimeOfIndex[pos];
    let length = 5000;
    requestForecast(startTime, length, Array.from(stationsInChart));
}
