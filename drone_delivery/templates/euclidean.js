const findDistance = () => {
  coordinates.forEach((outer, i) => {
    coordinates.forEach((inner, j) => {
      if (j === i) {
        return;
      }
      let distance = getDistanceFromLatLonInKm(outer.lat, inner.lan, outer.lng, inner.lng);
      console.log('Distance -> ', distance);
    });
  });
};

export const getDistanceFromLatLonInKm = (lat1, lon1, lat2, lon2) => {
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

// console.log(getDistanceFromLatLonInKm(28.632614391335558, 77.21963618777465, 28.63464840267726, 77.22714637301635));
