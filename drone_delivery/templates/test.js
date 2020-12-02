// This example adds an animated symbol to a polyline.
let coordinates = [];
let centerCoordinates = [];
let euclidean = [];
let map;
const labels = '@abcdefghijklmnopqrstuvwxyz';
const localWarehouse = '123456789';
let labelIndex = 0;
let centerIndex = 0;

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

const insertMarkerForCenters = (pos, map) => {
  new google.maps.Marker({
    position: pos,
    title: 'Local Warehouse',
    label: localWarehouse[centerIndex++ % localWarehouse.length],
    map: map,
  });
};

proceed.addEventListener('click', async (e) => {
  console.log('proceed');
  // send coordinates to server
  const response = await fetch('/submit', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ coordinates: coordinates, warehouse: coordinates[0] }),
  });
  let re = await response.json();

  document.getElementById('response').appendChild(document.createTextNode(JSON.stringify(re)));
  console.log('server response -> ', re);

  centers = re.centers;
  truckRoute = [];
  truckRouteFinal = [];
  // add marker for centers
  centers.forEach((d) => {
    let tempCoords = { lat: d[0], lng: d[1] };
    truckRoute.push(tempCoords);
    insertMarkerForCenters(tempCoords, map);
  });

  let directionsService = new google.maps.DirectionsService();
  let directionsDisplay = new google.maps.DirectionsRenderer({
    polylineOptions: {
      strokeColor: 'red',
    },
    suppressMarkers: true,
  });
  directionsDisplay.setMap(map);

  let waypoints = [];

  re.tsp_route.forEach((d) => {
    truckRouteFinal.push(truckRoute[d]);
    waypoints.push({ location: new google.maps.LatLng(truckRoute[d].lat, truckRoute[d].lng), stopover: true });
  });

  // waypoints.pop();

  // draw polyline for TSP Truck Route (warehouse -> 1,2,3 -> warehouse) ~! Partially Done
  // truckRoutePolyline = polyline(truckRouteFinal, '#FF00FF', map);
  // animateCircle(truckRoutePolyline);

  for (let i = 0; i < 3; i++) {
    route1 = re.route[i][0][0];
    route2 = re.route[i][0][1];

    // r1, r2 are the 2 drones in each cluster
    r1 = []; // polyline is drawn on r1, r2
    r2 = [];

    // draw polylines for Drone Routes (local cluster)
    route1.forEach((d) => {
      // debugger;
      let tCoordinate;
      if (d[0] === 'Depot') tCoordinate = truckRoute[i];
      else tCoordinate = coordinates[labels.indexOf(d[0])];
      r1.push(tCoordinate);
    });

    // r1.push(coordinates[labels.indexOf('@')]);
    r1.push(truckRoute[i]);

    route2.forEach((d) => {
      let tCoordinate;
      if (d[0] === 'Depot') tCoordinate = truckRoute[i];
      else tCoordinate = coordinates[labels.indexOf(d[0])];
      r2.push(tCoordinate);
    });
    r2.push(truckRoute[i]);

    line1 = polyline(r1, 'blue', map);
    line2 = polyline(r2, '#008080', map);

    animateCircle(line1);
    animateCircle(line2);
  }
  let originStation = new google.maps.LatLng(coordinates[0].lat, coordinates[0].lng);
  let finalStation = new google.maps.LatLng(truckRouteFinal[truckRouteFinal.length - 1].lat, truckRouteFinal[truckRouteFinal.length - 1].lng);
  finalStation = originStation;
  calculateAndDisplayRoute(directionsService, directionsDisplay, originStation, finalStation, waypoints);
});

const addLatLng = (e, map) => {
  // insert the coordinates into the map
  let _x_y = { lat: e.latLng.lat(), lng: e.latLng.lng() };
  coordinates.push(_x_y);
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
  const styledMapType = new google.maps.StyledMapType([
    {
      elementType: 'geometry',
      stylers: [
        {
          color: '#1d2c4d',
        },
      ],
    },
    {
      elementType: 'labels.text.fill',
      stylers: [
        {
          color: '#8ec3b9',
        },
      ],
    },
    {
      elementType: 'labels.text.stroke',
      stylers: [
        {
          color: '#1a3646',
        },
      ],
    },
    {
      featureType: 'administrative',
      elementType: 'geometry',
      stylers: [
        {
          visibility: 'off',
        },
      ],
    },
    {
      featureType: 'administrative.country',
      elementType: 'geometry.stroke',
      stylers: [
        {
          color: '#4b6878',
        },
      ],
    },
    {
      featureType: 'administrative.land_parcel',
      stylers: [
        {
          visibility: 'off',
        },
      ],
    },
    {
      featureType: 'administrative.land_parcel',
      elementType: 'labels.text.fill',
      stylers: [
        {
          color: '#64779e',
        },
      ],
    },
    {
      featureType: 'administrative.neighborhood',
      stylers: [
        {
          visibility: 'off',
        },
      ],
    },
    {
      featureType: 'administrative.province',
      elementType: 'geometry.stroke',
      stylers: [
        {
          color: '#4b6878',
        },
      ],
    },
    {
      featureType: 'landscape.man_made',
      elementType: 'geometry.stroke',
      stylers: [
        {
          color: '#334e87',
        },
      ],
    },
    {
      featureType: 'landscape.natural',
      elementType: 'geometry',
      stylers: [
        {
          color: '#023e58',
        },
      ],
    },
    {
      featureType: 'poi',
      stylers: [
        {
          visibility: 'off',
        },
      ],
    },
    {
      featureType: 'poi',
      elementType: 'geometry',
      stylers: [
        {
          color: '#283d6a',
        },
      ],
    },
    {
      featureType: 'poi',
      elementType: 'labels.text',
      stylers: [
        {
          visibility: 'off',
        },
      ],
    },
    {
      featureType: 'poi',
      elementType: 'labels.text.fill',
      stylers: [
        {
          color: '#6f9ba5',
        },
      ],
    },
    {
      featureType: 'poi',
      elementType: 'labels.text.stroke',
      stylers: [
        {
          color: '#1d2c4d',
        },
      ],
    },
    {
      featureType: 'poi.park',
      elementType: 'geometry.fill',
      stylers: [
        {
          color: '#023e58',
        },
      ],
    },
    {
      featureType: 'poi.park',
      elementType: 'labels.text.fill',
      stylers: [
        {
          color: '#3C7680',
        },
      ],
    },
    {
      featureType: 'road',
      elementType: 'geometry',
      stylers: [
        {
          color: '#304a7d',
        },
      ],
    },
    {
      featureType: 'road',
      elementType: 'labels',
      stylers: [
        {
          visibility: 'off',
        },
      ],
    },
    {
      featureType: 'road',
      elementType: 'labels.icon',
      stylers: [
        {
          visibility: 'off',
        },
      ],
    },
    {
      featureType: 'road',
      elementType: 'labels.text.fill',
      stylers: [
        {
          color: '#98a5be',
        },
      ],
    },
    {
      featureType: 'road',
      elementType: 'labels.text.stroke',
      stylers: [
        {
          color: '#1d2c4d',
        },
      ],
    },
    {
      featureType: 'road.highway',
      elementType: 'geometry',
      stylers: [
        {
          color: '#2c6675',
        },
      ],
    },
    {
      featureType: 'road.highway',
      elementType: 'geometry.stroke',
      stylers: [
        {
          color: '#255763',
        },
      ],
    },
    {
      featureType: 'road.highway',
      elementType: 'labels.text.fill',
      stylers: [
        {
          color: '#b0d5ce',
        },
      ],
    },
    {
      featureType: 'road.highway',
      elementType: 'labels.text.stroke',
      stylers: [
        {
          color: '#023e58',
        },
      ],
    },
    {
      featureType: 'transit',
      stylers: [
        {
          visibility: 'off',
        },
      ],
    },
    {
      featureType: 'transit',
      elementType: 'labels.text.fill',
      stylers: [
        {
          color: '#98a5be',
        },
      ],
    },
    {
      featureType: 'transit',
      elementType: 'labels.text.stroke',
      stylers: [
        {
          color: '#1d2c4d',
        },
      ],
    },
    {
      featureType: 'transit.line',
      elementType: 'geometry.fill',
      stylers: [
        {
          color: '#283d6a',
        },
      ],
    },
    {
      featureType: 'transit.station',
      elementType: 'geometry',
      stylers: [
        {
          color: '#3a4762',
        },
      ],
    },
    {
      featureType: 'water',
      elementType: 'geometry',
      stylers: [
        {
          color: '#0e1626',
        },
      ],
    },
    {
      featureType: 'water',
      elementType: 'labels.text',
      stylers: [
        {
          visibility: 'off',
        },
      ],
    },
    {
      featureType: 'water',
      elementType: 'labels.text.fill',
      stylers: [
        {
          color: '#4e6d70',
        },
      ],
    },
  ]);
  map = new google.maps.Map(document.getElementById('map'), {
    center: {
      lat: 28.6312756,
      lng: 77.2239758,
    },
    zoom: 14,
    clickableIcons: false,
    gestureHandling: 'greedy'
    // mapTypeId: 'terrain',
  });

  map.mapTypes.set('styled_map', styledMapType);
  map.setMapTypeId('styled_map');

  map.addListener('click', (e) => {
    addLatLng(e, map);
  });
}

function calculateAndDisplayRoute(directionsService, directionsDisplay, o, d, w) {
  directionsService.route(
    {
      origin: o,
      destination: d,
      waypoints: w,
      optimizeWaypoints: true,
      travelMode: 'DRIVING',
    },
    function (response, status) {
      if (status === 'OK') {
        directionsDisplay.setDirections(response);
      } else {
        window.alert('Directions request failed due to ' + status);
      }
    }
  );
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
