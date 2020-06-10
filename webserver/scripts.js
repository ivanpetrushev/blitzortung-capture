let mymap = L.map('mapid').setView([42.7389, 25.513], 8);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1
}).addTo(mymap);

let data = [];
let markers = [];
let currentIdx = 0;

fetch('data.json')
    .then(response => response.json())
    .then(json => {
        console.log('json is', json)
        data = json;
    })

cycleData = () => {
    currentIdx++;
    if (currentIdx >= Object.keys(data).length) {
        currentIdx = 0;
    }

    let key = Object.keys(data)[currentIdx];
    let selected = data[key];
    console.log('selected', key)
    for (let i in markers) {
        mymap.removeLayer(markers[i]);
    }

    for (let i in selected['cluster_centroids']) {
        let point = selected['cluster_centroids'][i];
        let marker = L.marker([point['lat'], point['lon']]).addTo(mymap);
        markers.push(marker);
    }
}

setInterval(cycleData, 2000);