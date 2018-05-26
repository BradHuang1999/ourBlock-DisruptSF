<template>
  <div class="md-layout max-100">
    <md-content class="md-layout-item md-size-30 max-100">
      <h4> Reports by Category </h4>
      <Linegraph />
      <h4> Reports by Hours of Day </h4>
      <Bargraph />
      <h2> Reports from last 7 days: {{ statsTotal }} </h2>
      <h4> Reports by Status from the last 7 days </h4>
      <Piegraph :pie-data="statsPie"/>
    </md-content>
    <md-content class="md-layout-item md-size-40 max-100">
      <Map
        @searchBounds="updateMap($event)"
        :markers="reportLocs"
      />
    </md-content>
    <md-content class="md-layout-item md-size-30 md-scrollbar max-100">
        <Card
          v-for="report in reports"
          :key="report._id"
        :loc-data="report"
        >
        </Card>
    </md-content>
  </div>
</template>

<script>
  import axios from 'axios';
  import Card from './components/Card.vue'
  import Map from './components/Map.vue'
  import Bargraph from './components/Bargraph.vue'
  import Linegraph from './components/Linegraph.vue'
  import Piegraph from './components/Piegraph.vue'
  import severity from '../lib/severity'

  export default {
    name: 'app',

    components: {
      Card, Map, Bargraph, Linegraph, Piegraph
    },

    data() {
      return {
        reports: [],
        reportLocs: [],
        statsTotal: 0,
        statsPie: [],
        lastBounds: {},
        lastCenter: {}
      }
    },

    mounted(){
      this.getStats();
      setInterval(this.getStats, 1000 * 60);
      setInterval(this.updateMap, 1000 * 10);
    },

    methods: {
      getStats() {
        axios.get('https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/stats')
          .then(stats => {
            this.statsTotal = stats.data.total;
            delete stats.data.total;
            this.statsPie = [
              ['Status', 'Count'],
              ["pending", stats.data["pending"]],
              ["in progress", stats.data["in progress"]],
              ["solved by public", stats.data["solved by public"]],
              ["solved by police", stats.data["pesolved by police"]]
            ]
          });
      },

      updateMap(events) {
        if (events){
          this.lastBounds = events.bounds;
          this.lastCenter = events.center;
        }
        axios.post('https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/search', {
          location: {
            latMin: this.lastBounds.latMin,
            latMax: this.lastBounds.latMax,
            lonMin: this.lastBounds.lonMin,
            lonMax: this.lastBounds.lonMax
          }
          // ,select: 'lat lon upvoterCount downvoterCount followerCount category time privacy status',
        })
        .then(locations => {
          this.reports = severity.getTopSeverity('police', Date.now(), this.lastCenter.lat, this.lastCenter.lng, locations.data, 25);
          this.reportLocs = this.reports.map(report => ({ position: { lat: report.lat, lng: report.lon } }));
          // navigator.geolocation.getCurrentPosition(position => {
          //   this.reports = severity.getTopSeverity('police', Date.now(), position.coords.latitude, position.coords.longitude, locations.data, 5);
          // });
        })
      }
    }
  }
</script>

<style scoped>
  body, html, .max-100{
    max-height: 100%;
    max-width: 100%;
    overflow-x: visible;
  }
</style>
