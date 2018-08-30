<template>
  <div>
    <gmap-map
      :center="center"
      :zoom="zoom"
      style="width:100%; height: 700px;"
      @bounds_changed="update($event)"
    >
      <gmap-marker
        :key="index"
        v-for="(m, index) in markers"
        :position="m.position"
        @click="center=m.position"
      ></gmap-marker>
    </gmap-map>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "GoogleMap",
  data() {
    return {
      center: { lat: 37.7833570391, lng: -122.4167107338 },
      zoom: 18,
      markers: [],
    };
  },

  mounted() {
    // console.log(this.getBounds());
    this.getPins(-122.4177107338, -122.4157107338, 37.7823570391, 37.7843570391);
  },

  methods: {
    update(event) {
      // console.log(event.b.b, event.b.f, event.f.b, event.f.f);
      this.getPins(event.b.b, event.b.f, event.f.b, event.f.f);
    },

    getPins(lonMin, lonMax, latMin, latMax) {
      axios.post('https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/search', {
        location: {
          latMin: latMin,
          latMax: latMax,
          lonMin: lonMin,
          lonMax: lonMax
        },
        select: 'lat lon',
      })
      .then(locations => {
          console.log("locations", locations);
          locations.data.forEach(location => {
            this.markers.push({
              position: {
                lat: location.lat,
                lng: location.lon
              }
            })
          });
      })
    },

    addMarker() {
      if (this.currentPlace) {
        const marker = {
          lat: this.currentPlace.geometry.location.lat(),
          lng: this.currentPlace.geometry.location.lng()
        };
        this.markers.push({ position: marker });
        this.places.push(this.currentPlace);
        this.center = marker;
      }
    },

    geolocate: function() {
      navigator.geolocation.getCurrentPosition(position => {
        this.center = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
      });
    }
  }
};
</script>
