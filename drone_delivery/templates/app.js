let poly;
let map;
let coordinates = [];
let euclidean = [];

let proceed = document.getElementById('draw-polygon');

proceed.addEventListener('click', (e) => {
  console.log('proceed');
  insertPolygon();
  findDistance();
});

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 16,
    center: { lat: 28.634723, lng: 77.227082 }, // Center the map on Chicago, USA.
  });
  console.log('initmap()');
  map.addListener('click', addLatLng);
}

const addLatLng = (e) => {
  // insert the coordinates into the map
  let _x_y = { lat: e.latLng.lat(), lng: e.latLng.lng() };
  coordinates.push(_x_y);
  console.log('inserted -> ', coordinates);
  insertMarker(e.latLng);
  // draw the marker on it
};

const insertMarker = (pos) => {
  console.log(pos);
  new google.maps.Marker({
    position: pos,
    title: 'Hey',
    map: map,
  });
};

const insertPolygon = () => {
  const polygon = new google.maps.Polygon({
    paths: coordinates,
    strokeColor: '#FF0000',
    strokeOpacity: 0.8,
    strokeWeight: 3,
    fillColor: '#FF0000',
    fillOpacity: 0.35,
  });
  polygon.setMap(map);
};

const findDistance = () => {
  coordinates.forEach((outer, i) => {
    euclidean.push([]);
    coordinates.forEach((inner, j) => {
      // if (j === i) {
      // return;
      // }
      let distance = getDistanceFromLatLonInKm(outer.lat, outer.lng, inner.lat, inner.lng);
      euclidean[i].push(distance);
      // store in an adjacency list
    });
  });
  console.log(euclidean);
};

const getDistanceFromLatLonInKm = (lat1, lon1, lat2, lon2) => {
  var R = 6371; // Radius of the earth in km
  var dLat = deg2rad(lat2 - lat1); // deg2rad below
  var dLon = deg2rad(lon2 - lon1);
  var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  var d = R * c; // Distance in km
  return d * 1000;
};

const deg2rad = (deg) => {
  return deg * (Math.PI / 180);
};
