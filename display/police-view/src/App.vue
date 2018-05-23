<template>
  <div class="md-layout">
    <md-content class="md-layout-item md-size-30">
      <md-content class="md-elevation-2">
        <h4 style="text-align: center;"> Crimes by Time, Categorized</h4>
        <Linegraph />
      </md-content>
      <md-content class="md-elevation-2">
        <h4 style="text-align: center;"> Total Count Crimes per Hour </h4>
        <Bargraph />
      </md-content>
      <!-- <h2> Reports from last 7 days: {{ statsTotal }} </h2> -->
      <md-content class="md-elevation-2">
        <h4 style="text-align: center;"> Crime Category Breakdown </h4>
        <Donutgraph />
      </md-content>
      <md-content class="md-elevation-2">
        <h4 style="text-align: center;"> Crime by Location </h4>
        <Scattergraph />
      </md-content>
      <md-content class="md-elevation-2">
        <h4 style="text-align: center;"> Crime Status Breakdown </h4>
        <Piegraph :pie-data="statsPie"/>
      </md-content>
    </md-content>
    <md-content class="md-layout-item md-size-40">
      <center><img src="./assets/frontPageLogoClear.png" width="300" style="padding: 10px"></center>
      {{selectedId}}
      <Map
        @markerClicked="selectCard($event)"
        @searchBounds="updateMap($event)"
        :markers="reportLocs"
        :selectedId="selectedId"
      />
      <Nodes></Nodes>
    </md-content>
    <md-content class="md-layout-item md-size-30 md-scrollbar" style="position: relative; overflow: auto;" id="screenHeightCustom">
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
  import Donutgraph from './components/Donutgraph.vue'
  import Scattergraph from './components/Scattergraph.vue'
  import severity from '../lib/severity'
  import Nodes from '../nodes/src/example/Example.vue'

  window.onload = function() {
    var height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
    var myDiv = document.getElementById("screenHeightCustom");
    myDiv.style.height = height + "px";
  }

  export default {
    name: 'app',

    components: {
      Card, Map, Bargraph, Linegraph, Piegraph, Donutgraph, Scattergraph, Nodes
    },

    data() {
      return {
        reports: [],
        reportLocs: [],
        statsTotal: 0,
        statsPie: [],
        lastBounds: {},
        lastCenter: {},
        selectedId: 0
      }
    },

    mounted(){
      this.getStats();
      setInterval(this.getStats, 1000 * 60);
      setInterval(this.updateMap, 1000 * 10);
    },

    methods: {
      selectCard(id) {
        console.log(id);
        this.selectedId = id;
        this.getSelectedToTop();
      },

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
          this.getSelectedToTop();
          console.log(this.reports);
          this.reportLocs = this.reports.map(report => ({ position: { lat: report.lat, lng: report.lon }, id: report._id }));
          // navigator.geolocation.getCurrentPosition(position => {
          //   this.reports = severity.getTopSeverity('police', Date.now(), position.coords.latitude, position.coords.longitude, locations.data, 5);
          // });
        })
      },

      getSelectedToTop() {
        var selectedReportIndex = this.reports.findIndex(report => report._id === this.selectedId);
        if (selectedReportIndex > 0) {
          var selectedReport = this.reports[selectedReportIndex];
          this.reports.splice(selectedReportIndex, 1);
          this.reports.unshift(selectedReport);
        }
      }
    }
  }
</script>

<style scoped>
  .md-elevation-2 {
    padding: 10px;
    margin: 10px;
  }
</style>
