<template>
  <div class="md-layout max-100">
    <div class="md-layout-item md-size-25 max-100">
      <Linegraph />
      <Bargraph />
      <h2>Reports from last 7 days</h2>
      <Piegraph />
    </div>
    <div class="md-layout-item md-size-40 max-100">
      <Map
        @searchBounds="searchBounds($event)"
      />
    </div>
    <div class="md-layout-item md-size-35 md-scrollbar max-100">
        <Card
          v-for="report in reports"
          :key="report._id"
          :loc-data="report">
        </Card>
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import Card from './components/Card.vue'
  import Map from './components/Map.vue'
  import Bargraph from './components/Bargraph.vue'
  import Linegraph from './components/Linegraph.vue'
  import Piegraph from './components/Piegraph.vue'

  export default {
    name: 'app',

    components: {
      Card, Map, Bargraph, Linegraph, Piegraph
    },

    data() {
      return {
        reports: [1, 2, 3]
      }
    },

    methods: {
      searchBounds(bounds){
        axios.post('https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/search', {
          location: {
            latMin: bounds.latMin,
            latMax: bounds.latMax,
            lonMin: bounds.lonMin,
            lonMax: bounds.lonMax
          },
          select: 'lat lon upvoterCount downvoterCount followerCount category time privacy status',
        })
        .then(locations => {
          // console.log(locations.data);
          this.reports = locations.data.slice(0,3);
        })
      }
    }
  }
</script>

<style>
  body, html, .max-100{
    height: 100%;
    width: 100%;
    overflow-x: visible;
  }
</style>
