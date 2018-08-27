<template>
  <div>
    <gmap-map
      :center="center"
      :zoom="zoom"
      style="width:100%; height: 700px;"
      @bounds_changed="changeBounds($event)"
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
      prevBounds: {},
      currBounds: {
        lonMin: -122.4177107338,
        lonMax: -122.4157107338,
        latMin: 37.7823570391,
        latMax: 37.7843570391 
      }
    };
  },

  mounted() {
    setInterval(() => {
      if (this.prevBounds !==  this.currBounds){
        this.getPins(this.currBounds);
        this.$emit('searchBounds', this.currBounds)
        this.prevBounds = this.currBounds;
      }
    }, 1000);
  },

  methods: {
    changeBounds(event) {
      if (event){
        this.currBounds = {
          lonMin: event.b.b,
          lonMax: event.b.f,
          latMin: event.f.b,
          latMax: event.f.f
        };
      }
    },

    getPins(bounds) {
      axios.post('https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/search', {
        location: {
          latMin: bounds.latMin,
          latMax: bounds.latMax,
          lonMin: bounds.lonMin,
          lonMax: bounds.lonMax
        },
        select: 'lat lon upvoterCount downvoterCount followerCount category time',
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
