
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
            text: 'Chart.js Line Chart',
        },
        showTooltips: false,
        hover: false,
        animation:{
            duration: 0
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

document.getElementById('randomizeData').addEventListener('click', function() {
    config.data.datasets.forEach(function(dataset) {
        dataset.data = dataset.data.map(function() {
            return randomValue();
        });
    });

    window.myLine.update();
});

let colorNames = Object.keys(window.chartColors);
document.getElementById('addDataset').addEventListener('click', function() {
    let colorName = colorNames[config.data.datasets.length % colorNames.length];
    let newColor = window.chartColors[colorName];
    let newDataset = {
        label: 'Dataset ' + config.data.datasets.length,
        backgroundColor: newColor,
        borderColor: newColor,
        data: [],
        fill: false,
    };

    for (let index = 0; index < config.data.labels.length; ++index) {
        newDataset.data.push(randomValue());
    }

    config.data.datasets.push(newDataset);
    window.myLine.update();
});

document.getElementById('addData').addEventListener('click', function() {
    if (config.data.datasets.length > 0) {
        let month = MONTHS[config.data.labels.length % MONTHS.length];
        config.data.labels.push(month);

        config.data.datasets.forEach(function(dataset) {
            dataset.data.push(randomValue());
        });

        window.myLine.update();
    }
});

document.getElementById('removeDataset').addEventListener('click', function() {
    config.data.datasets.splice(0, 1);
    window.myLine.update();
});

document.getElementById('removeData').addEventListener('click', function() {
    config.data.labels.splice(-1, 1); // remove the label first

    config.data.datasets.forEach(function(dataset) {
        dataset.data.pop();
    });

    window.myLine.update();
});

/* exported replaceChart */
/**
 * Draw a new graph, removing the previous one
 * @param {Array} labels
 * @param {Array} occupancy
 * @param {String} polygonId
 * @param {int} timeDeltaS
 */
function replaceChart(labels, occupancy, selectionType, selectionId, timeDeltaS) {
    // get new color in list
    let colorName = colorNames[config.data.datasets.length % colorNames.length];
    let newColor = window.chartColors[colorName];
    let minutes = timeDeltaS / 60;
    let hours = minutes / 60;
    let timeStr;
    if (hours >= 1) {
        timeStr = hours + ' hour' + (hours == 1 ? '' : 's');
    } else {
        timeStr = minutes + ' minute' + (minutes == 1 ? '' : 's');
    }

    if (selectionType === 'station') {

    }

    let newDataset = {
        id: selectionId,
        label: 'Bike occupancy averaged for every ' + timeStr + ' for '
        + (selectionType === 'polygon'?
            polygonLabelMap[selectionId] : 'Station ' + selectionId),
        backgroundColor: newColor,
        borderColor: newColor,
        data: [],
        fill: false,
    };

    console.log('drawing chart with data:');
    // empty the previous graphs
    // while (config.data.datasets.length) {
    //     config.data.datasets.pop();
    // }
    //
    // while (config.data.labels.length) {
    //     config.data.labels.pop();
    // }

    if (config.data.labels.length === 0) {
        for (let index = 0; index < labels.length; ++index) {
            config.data.labels.push(labels[index]);
        }
    }

    for (let index = 0; index < occupancy.length; ++index) {
        newDataset.data.push(occupancy[index]);
    }

    config.data.datasets.push(newDataset);
    window.myLine.update();
}

/* exported removeDatasetFromChart */

function removeDatasetFromChart(selectionId) {
    let removalIndex = config.data.datasets.indexOf(
        config.data.datasets.filter(
            function(dataObject) {
                return dataObject.id === selectionId;
    })[0]);
    if (removalIndex >= 0) {
        config.data.datasets.splice(removalIndex, 1);
        window.myLine.update();
    }
}
