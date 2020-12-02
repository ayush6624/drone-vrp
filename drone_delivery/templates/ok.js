function initMap() {
  console.log('here');
  var map = new google.maps.Map(document.getElementById('map_canvas'), {
    center: new google.maps.LatLng(28.613767, 77.21178),
    zoom: 13,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
  });
  var lineSymbol = {
    path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW,
    scale: 4, // change the size
    strokeColor: '#393',
  };

  // test.js
  var lineSymbolAnother = {
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
        icon: lineSymbolAnother,
        offset: '100%',
      },
    ],
    map: map,
  });
  animateCircle(line);
  // end

  var directionsService = new google.maps.DirectionsService();
  var directionsDisplay = new google.maps.DirectionsRenderer({
    map: map,
    preserveViewport: true,
  });
  directionsService.route(
    {
      origin: new google.maps.LatLng(28.635378, 77.226876),
      destination: new google.maps.LatLng(28.635378, 77.226876),
      waypoints: [
        {
          stopover: false,
          location: new google.maps.LatLng(28.612689, 77.22769),
        },
        {
          stopover: false,
          location: new google.maps.LatLng(28.613767, 77.21178),
        },
      ],
      travelMode: google.maps.TravelMode.DRIVING,
    },
    function (response, status) {
      if (status === google.maps.DirectionsStatus.OK) {
        // directionsDisplay.setDirections(response);
        var polyline = new google.maps.Polyline({
          path: [],
          strokeColor: '#0000FF',
          strokeWeight: 3,
          icons: [
            {
              icon: lineSymbol,
              offset: '100%',
            },
          ],
        });
        var bounds = new google.maps.LatLngBounds();

        var legs = response.routes[0].legs;
        for (i = 0; i < legs.length; i++) {
          var steps = legs[i].steps;
          for (j = 0; j < steps.length; j++) {
            var nextSegment = steps[j].path;
            for (k = 0; k < nextSegment.length; k++) {
              polyline.getPath().push(nextSegment[k]);
              bounds.extend(nextSegment[k]);
            }
          }
        }

        polyline.setMap(map);
        animateCircle(polyline);
      } else {
        window.alert('Directions request failed due to ' + status);
      }
    }
  );
}

function animateCircle(line) {
  var count = 0;
  window.setInterval(function () {
    count = (count + 1) % 200; // change this to 1000 to only show the line once
    var icons = line.get('icons');
    icons[0].offset = count / 2 + '%';
    line.set('icons', icons);
  }, 50); // change this value to change the speed
}
