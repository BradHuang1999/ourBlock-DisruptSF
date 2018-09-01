<template>
  <div class="md-layout max-100">
    <md-content class="md-layout-item md-size-30 max-100">

      <h4 style="text-align: center;"> Crimes by Time, Categorized</h4>
      <div class="boxThing"><Linegraph /></div>
      <h4 style="text-align: center;"> Total Count Crimes per Hour </h4>
      <div class="boxThing"><Bargraph /></div>
      <!-- <h2> Reports from last 7 days: {{ statsTotal }} </h2> -->
      <h4 style="text-align: center;"> Crime Category Breakdown </h4>
      <div class="boxThing"> <Donutgraph /></div>
      <h4 style="text-align: center;"> Crime by Location </h4>
      <div class="boxThing"> <Scattergraph /></div>
      <h4 style="text-align: center;"> Crime Status Breakdown </h4>
      <div class="boxThing"><Piegraph :pie-data="statsPie"/></div>

    </md-content>

    <md-content class="md-layout-item md-size-40 max-100">
      <img src="logo.png">
      {{selectedId}}
      <Map
        @markerClicked="selectCard($event)"
        @searchBounds="updateMap($event)"
        :markers="reportLocs"
        :selectedId="selectedId"
      />
      <Nodes></Nodes>
    </md-content>
    <md-content class="md-layout-item md-size-30 md-scrollbar max-100" style="position: relative; overflow: auto;" id="screenHeightCustom">
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
  body, html, .max-100{
    max-height: 100%;
    max-width: 100%;
    overflow-x: visible;
    bakckground: white;
  }
  .boxThing{
    -webkit-box-shadow: 0 1px 2px #777;
    -moz-box-shadow: 0 2px 1px #777;
    box-shadow: 0 2px 1px #777;
    z-index: 10000;
  }
</style>
