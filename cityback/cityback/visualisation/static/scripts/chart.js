var MONTHS = ['January', 'February', 'March', 'April', 'May',
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

function randomValue() {
    return Math.round(Math.random() * 200 - 100)

}
var config = {
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
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true,
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

var colorNames = Object.keys(window.chartColors);
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

function replaceChart(labels, occupancy, time_delta_s){
    // get new color in list
    let colorName = colorNames[config.data.datasets.length % colorNames.length];
    let newColor = window.chartColors[colorName];
    let minutes = time_delta_s / 60;
    let hours = minutes / 60;

    if(hours >= 1)
        time_str = hours + ' hour'  + (hours == 1 ? '' : 's');
    else
        time_str = minutes + ' minute' + (minutes == 1 ? '' : 's');

    let newDataset = {
        label: 'Bike occupancy averaged for every ' + time_str,
        backgroundColor: newColor,
        borderColor: newColor,
        data: [],
        fill: false,
    };

    console.log("drawing chart with data:")
    // empty the previous graphs
    while(config.data.datasets.length)
        config.data.datasets.pop();

    while(config.data.labels.length)
        config.data.labels.pop();

    for (let index = 0; index < labels.length; ++index) {
        config.data.labels.push(labels[index]);
    }

    for (let index = 0; index < occupancy.length; ++index) {
        newDataset.data.push(occupancy[index]);
    }

    config.data.datasets.push(newDataset);
    window.myLine.update();
}
