// This example adds an animated symbol to a polyline.
let coordinates = [];
let euclidean = [];

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
  console.log('server response -> ', re);
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
    title: 'Hey',
    map: map,
  });
};

function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
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

  var lineSymbol = {
    path: google.maps.SymbolPath.CIRCLE,
    scale: 5, // change the size
    strokeColor: '#393',
  };

  var line = new google.maps.Polyline({
    path: [
      {
        lat: 28.6312756,
        lng: 77.2239758,
      },
      {
        lat: 28.6266846,
        lng: 77.2397423,
      },
      {
        lat: 28.6226552,
        lng: 77.2092844,
      },
      {
        lat: 28.6312756,
        lng: 77.2239758,
      },
    ],
    strokeColor: '#FF0000',
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

  animateCircle(line);
}

// Use the DOM setInterval() function to change the offset of the symbol
// at fixed intervals.
function animateCircle(line) {
  var count = 0;
  window.setInterval(function () {
    count = (count + 1) % 200; // change this to 1000 to only show the line once
    var icons = line.get('icons');
    icons[0].offset = count / 2 + '%';
    line.set('icons', icons);
  }, 50); // change this value to change the speed
}
