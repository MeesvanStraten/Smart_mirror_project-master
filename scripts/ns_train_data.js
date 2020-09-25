const Store = require('electron-store');
const store = new Store();
const apiKey = 'zuWYyA1rEZ5YGVeeIgyCx5nydhJvW1f3lj5FA9Ra';
/* jshint ignore:start */

function storeInCache(key, data, ttl) {
    store.set(key, {
        data:    data,
        expires: Date.now() + (ttl * 1000) // sec naar ms
    });
    return data;
}
function getFromCache(key) {
    let storeData = store.get(key);
    if(storeData.expires < Date.now()) return false;
    return storeData.data;
}

const userAction = async () => {

    let urls       = {
        departures: 'https://ns-api.nl/reisinfo/api/v2/departures?station=',
    };
    let stationID  = 'EHV';
    let headers    = new Headers();
    headers.append('x-api-key', apiKey);
    let request = new Request(urls.departures + stationID, {
        headers: headers
    });
    fetch(request).then(response => {
        return response.json();
    }).then(json => {
        updateView(storeInCache('ns.departures', json, 60));
    }).catch(error => {
       console.error(error);
    });
};

function updateView(data) {

    for(let index in data.payload.departures) {
        console.log(data.payload.departures[index]);
    }
}

setInterval(function () {
    let cache = getFromCache('ns.departures');
    if(cache === false) {
        userAction();
    } else {
        updateView(cache);
    }
    //userAction();
    //console.log(store.get('ns.departures'))
}, 10000);
