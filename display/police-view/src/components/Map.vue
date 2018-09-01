<template>
  <div>
    <gmap-map
      :center="center"
      :zoom="zoom"
      style="width:100%; height: 550px; margin=8px"
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

  props: ['markers'],

  data() {
    let center = { lat: 37.785078, lng: -122.400497 };
    // navigator.geolocation.getCurrentPosition(position => {
    //   center = {
    //     lat: position.coords.latitude,
    //     lng: position.coords.longitude
    //   };
    // });
    return {
      center: center,
      zoom: 16,
      // markers: this.reportLocs,//this.reports.map(report => { return ({ position: { lat: report.lat, lng: report.lng } }) }),
      prevBounds: {},
      currBounds: {
        lonMin: center.lng - 0.005,
        lonMax: center.lng + 0.005,
        latMin: center.lat - 0.005,
        latMax: center.lat + 0.005
      }
    };
  },

  mounted() {
    setInterval(() => {
      if (this.prevBounds !== this.currBounds){
        this.$emit('searchBounds', { bounds: this.currBounds, center: this.center });
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
        locations.data.forEach(location => {
          this.markers.push({
            position: {
              lat: location.lat,
              lng: location.lon
            }
          })
        });
      })
    }
  }
};
</script>
