function getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2) {
  var R = 6371; // Radius of the earth in km
  var dLat = deg2rad(lat2 - lat1); // deg2rad below
  var dLon = deg2rad(lon2 - lon1);
  var a = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  var d = R * c; // Distance in km
  return d;
}

function deg2rad(deg) {
  return deg * (Math.PI / 180);
}

console.log(getDistanceFromLatLonInKm(28.632614391335558, 77.21963618777465, 28.63464840267726, 77.22714637301635));

// [Log] inserted ->  – [{lat: 28.63521480479436, lng: 77.22622369311523}, {lat: 28.607002692906335, lng: 77.22725366137695}] (2) (app.js, line 24)

// [Log] inserted ->  – [{lat: 28.632614391335558, lng: 77.21963618777465}, {lat: 28.63464840267726, lng: 77.22714637301635}] (2) (app.js, line 48)
