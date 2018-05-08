<template>
  <div>
    <iframe 
      :style="'width:100%; height: ' + screenHeight / 5 * 2 + 'px; margin=8px'"
      scrolling="no"
      frameborder="no"
      :src="'https://fusiontables.google.com/embedviz?q=select+col1%2C+col2+from+1SM4l-pk3LP6NiRHTCcUob6ddg3Xrgc4o55-0-F_5+limit+1000&amp;viz=HEATMAP&amp;h=true&amp;lat=37.786570&amp;lng=-122.402&amp;t=3&amp;z=13&amp;l=col1&amp;y=2&amp;tmplt=2&amp;hmd=true&amp;hmg=%2366ff0000%2C%2393ff00ff%2C%23c1ff00ff%2C%23eeff00ff%2C%23f4e300ff%2C%23f4e300ff%2C%23f9c600ff%2C%23ffaa00ff%2C%23ff7100ff%2C%23ff3900ff%2C%23ff0000ff&amp;hmo=0.6&amp;hmr=10&amp;hmw=0&amp;hml=TWO_COL_LAT_LNG'">
    </iframe>
    <gmap-map
      :center="mapCenter"
      :zoom="zoom"
      :style="'zoom:70%; width:100%; height:' + screenHeight * 3 / 5 * 10 / 7 + 'px; margin=8px'"
      @center_changed="center={lat: $event.lat(), lng: $event.lng()}"
      @bounds_changed="changeBounds($event)"
    >
      <gmap-marker
        :key="marker.id"
        v-for="marker in markers"
        :position="marker.position"
        :label="selectedId === marker.id ? '!' : ''"
        @click="markerClicked($event, marker.id)"
      >
      </gmap-marker>
    </gmap-map>
  </div>
</template>

<script>
export default {
  name: "GoogleMap",

  props: ['mapCenter', 'markers', "selectedId", "screenHeight"],

  data() {
    return {
      center: this.mapCenter,
      zoom: 16,
      prevBounds: {},
      currBounds: {
        lonMin: this.mapCenter.lng - 0.005,
        lonMax: this.mapCenter.lng + 0.005,
        latMin: this.mapCenter.lat - 0.005,
        latMax: this.mapCenter.lat + 0.005
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
    markerClicked(event, id) {
      console.log(event, id)
      this.$emit('markerClicked', id);
    },

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
