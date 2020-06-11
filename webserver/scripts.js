let mymap = L.map('mapid').setView([42.7389, 25.513], 7);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
}).addTo(mymap);
L.control.scale().addTo(mymap);

let data = [];
let markers = [];
let currentIdx = -1;

fetch('data.json')
    .then(response => response.json())
    .then(json => {
        data = json;
        document.getElementById('slider').max = Object.keys(data).length - 1;
    })

cycleData = () => {
    for (let i in markers) {
        mymap.removeLayer(markers[i]);
    }

    currentIdx++;
    if (currentIdx >= Object.keys(data).length) {
        currentIdx = -1;
    }
    if (currentIdx === -1) {
        document.getElementById('title').innerHTML = 'Begin';
        console.log('===========================');
        return;
    }

    displayData(currentIdx);

    let oldValue = document.getElementById('slider').value;
    document.getElementById('slider').value = currentIdx;
}

let interval = setInterval(cycleData, 1000);

onSliderChanged = (value) => {
    clearInterval(interval);
    displayData(value);
    currentIdx = value;
}

displayData = (i) => {
    for (let i in markers) {
        mymap.removeLayer(markers[i]);
    }

    let key = Object.keys(data)[i];
    let selected = data[key];
    document.getElementById('title').innerHTML = key;

    for (let i in selected['cluster_centroids']) {
        let point = selected['cluster_centroids'][i];
        let marker = L.marker([point['lat'], point['lon']]).addTo(mymap);
        markers.push(marker);
    }
}

goBack = () => {
    clearInterval(interval);
    currentIdx--;
    if (currentIdx < 0) {
        currentIdx = 0;
    }
    displayData(currentIdx);
}

goForth = () => {
    clearInterval(interval);
    currentIdx++;
    if (currentIdx > Object.keys(data).length - 1) {
        currentIdx = Object.keys(data).length - 1;
    }
    displayData(currentIdx);
}