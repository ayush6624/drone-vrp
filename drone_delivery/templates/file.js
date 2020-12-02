/* Draw multiple polylines and connect them with markers
let poly;
let map;

function initMap() {
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 16,
    center: { lat: 28.634723, lng: 77.227082 }, // Center the map on Chicago, USA.
  });
  poly = new google.maps.Polyline({
    strokeColor: '#000000',
    strokeOpacity: 1.0,
    strokeWeight: 9,
  });
  poly.setMap(map);
  // Add a listener for the click event
  map.addListener('click', addLatLng);
}

// Handles click events on a map, and adds a new point to the Polyline.
function addLatLng(event) {
  const path = poly.getPath();
  // Because path is an MVCArray, we can simply append a new coordinate
  // and it will automatically appear.
  path.push(event.latLng);
  // Add a new marker at the new plotted point on the polyline.
  new google.maps.Marker({
    position: event.latLng,
    title: '#' + path.getLength(),
    map: map,
  });
}

*/

/*
Fill the drone's flying area with a polygon
*/
