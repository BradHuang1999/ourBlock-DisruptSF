<template>
  <div>
    <gmap-map
      :center="mapCenter"
      :zoom="zoom"
      style="width:100%; height: 550px; margin=8px"
      @center_changed="center={lat: $event.lat(), lng: $event.lng()}"
      @bounds_changed="changeBounds($event)"
    >
      <gmap-marker
        :key="marker._id"
        v-for="marker in markers"
        :position="marker.position"
      >
        <!-- <GmapInfoWindow opened="openWindowKeys.include(marker._id)" @closeclick="openWindowKeys.pull(marker._id)">
          hey
        </GmapInfoWindow> -->
      </gmap-marker>
    </gmap-map>
  </div>
</template>

<script>
// import axios from 'axios';

export default {
  name: "GoogleMap",

  props: ['markers'],

  data() {
    let mapCenter = { lat: 37.786570, lng: -122.402 };
    // navigator.geolocation.getCurrentPosition(position => {
    //   center = {
    //     lat: position.coords.latitude,
    //     lng: position.coords.longitude
    //   };
    // });
    return {
      mapCenter: mapCenter,
      center: mapCenter,
      zoom: 16,
      prevBounds: {},
      currBounds: {
        lonMin: mapCenter.lng - 0.005,
        lonMax: mapCenter.lng + 0.005,
        latMin: mapCenter.lat - 0.005,
        latMax: mapCenter.lat + 0.005
      },
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
    }
  }
};
</script>
