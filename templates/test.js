// This example adds an animated symbol to a polyline.
let coordinates = [];
let euclidean = [];
let map;
const labels = '@abcdefghijklmnopqrstuvwxyz';
let labelIndex = 0;

const polyline = (coords, color, map) => {
  let lineSymbol = {
    path: google.maps.SymbolPath.CIRCLE,
    scale: 5, // change the size
    strokeColor: '#393',
  };
  let line = new google.maps.Polyline({
    path: coords,
    strokeColor: color,
    strokeOpacity: 1.0,
    strokeWeight: 2, // change this value to show / hide the line
    icons: [
      {
        icon: lineSymbol,
        offset: '100%',
      },
    ],
    map: map,
  });
  return line;
};

let proceed = document.getElementById('draw-polygon');

proceed.addEventListener('click', async (e) => {
  console.log('proceed');
  // send coordinates to server
  const response = await fetch('/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ coordinates: coordinates }),
  });
  let re = await response.json();

  document.getElementById('response').appendChild(document.createTextNode(JSON.stringify(re)));
  console.log('server response -> ', re);

  route1 = re.route[0];
  route2 = re.route[1];
  r1 = [];
  r2 = [];
  route1.forEach((d) => {
    if (d[0] === 'Depot') d[0] = '@';
    let tCoordinate = coordinates[labels.indexOf(d[0])];
    r1.push(tCoordinate);
  });
  r1.push(coordinates[labels.indexOf('@')]);
  console.log(r1);

  route2.forEach((d) => {
    if (d[0] === 'Depot') d[0] = '@';
    let tCoordinate = coordinates[labels.indexOf(d[0])];
    r2.push(tCoordinate);
  });
  r2.push(coordinates[labels.indexOf('@')]);
  console.log(r2);

  line1 = polyline(r1, 'FF0000', map);
  line2 = polyline(r2, '008080', map);

  animateCircle(line1);
  animateCircle(line2);
});

const addLatLng = (e, map) => {
  // insert the coordinates into the map
  let _x_y = { lat: e.latLng.lat(), lng: e.latLng.lng() };
  coordinates.push(_x_y);
  console.log('coordinates[] -> ', coordinates);
  insertMarker(e.latLng, map);
  // draw the marker on it
};

const insertMarker = (pos, map) => {
  console.log('insertMarker');
  new google.maps.Marker({
    position: pos,
    title: 'Point ' + coordinates.length,
    label: labels[labelIndex++ % labels.length],
    map: map,
  });
};

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    center: {
      lat: 28.6312756,
      lng: 77.2239758,
    },
    zoom: 14,
    // mapTypeId: 'terrain',
  });
  map.addListener('click', (e) => {
    addLatLng(e, map);
  });
}

// Use the DOM setInterval() function to change the offset of the symbol at fixed intervals.
function animateCircle(line) {
  var count = 0;
  window.setInterval(function () {
    count = (count + 1) % 200; // change this to 1000 to only show the line once
    var icons = line.get('icons');
    icons[0].offset = count / 2 + '%';
    line.set('icons', icons);
  }, 50); // change this value to change the speed
}
