<template>
  <div class="md-layout">
    <md-content 
      class="md-layout-item md-size-30"
      style="position: relative; overflow: auto;"
      id="leftTab"
    >
      <center>
        <img src="./assets/frontPageLogoClear.png" width="150" style="padding: 10px">
      </center>
      <md-content class="md-elevation-2">
        <h4> Crimes by Time, Categorized</h4>
        <Linegraph />
      </md-content>
      <md-content class="md-elevation-2">
        <h4> Distributed Node Network Graph </h4>
        <Nodes style="zoom: 56%;"></Nodes>
      </md-content>
      <md-content class="md-elevation-2">
        <h4> Neural Network Training Rate </h4>
        <div id="trainingStep">Training Step: {{iter}} </div>  
        <img style="height:250px;" :src="require('./assets/neuralnetgraph.gif')">
      </md-content>
      <md-content class="md-elevation-2">
        <h4> Crime Category Breakdown </h4>
        <Donutgraph />
      </md-content>
      <md-content class="md-elevation-2">
        <h4> Crime Count Per Hour </h4>
        <Bargraph />
      </md-content>
      <md-content class="md-elevation-2">
        <h4> Crime by Location </h4>
        <Scattergraph />
      </md-content>
    </md-content>

    <md-content 
      class="md-layout-item md-size-40"
      id="middleTab"
    >
      <Map
        @markerClicked="selectCard($event)"
        @searchBounds="updateMap($event)"
        :markers="reportLocs"
        :selectedId="selectedId"
        :screenHeight="screenHeight"
        :mapCenter="location"
      />
    </md-content>

    <md-content class="md-layout-item md-size-30 md-scrollbar">
      <md-content 
        style="position: relative; overflow: auto;"
        id="rightTab"
      >
        <Card
          v-for="report in reports"
          :key="report._id"
          :loc-data="report"
          :selectedId="selectedId"
          :screenHeight="screenHeight"
        ></Card>
      </md-content>
      <md-content 
        class="md-elevation-2"
        style="margin-bottom=0"
      >
        <h4> Crime Status Breakdown </h4>
        <Piegraph :pie-data="statsPie"/>
        <!-- <h2> Reports from last 7 days: {{ statsTotal }} </h2> -->
      </md-content>
    </md-content>
  </div>
</template>

<script>
  import Vue from 'vue'
  import axios from 'axios';
  import Card from './components/Card.vue'
  import Map from './components/Map.vue'
  import Bargraph from './components/Bargraph.vue'
  import Linegraph from './components/Linegraph.vue'
  import Piegraph from './components/Piegraph.vue'
  import Donutgraph from './components/Donutgraph.vue'
  import Scattergraph from './components/Scattergraph.vue'
  import Nodes from './components/blockchain-nodes/example/Example.vue'

  window.onload = function() {
    this.screenHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
    var leftTab = document.getElementById("leftTab");
    var rightTab = document.getElementById("rightTab");
    leftTab.style.height = this.screenHeight + "px";
    rightTab.style.height = this.screenHeight - 198 + "px";
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
        selectedId: '',
        screenHeight: 0,
        iter: 0,
        location: {
          lat: 37.786570,
          lng: -122.402
        }
      }
    },

    mounted(){
      this.screenHeight = window.innerHeight;
      this.getStats();
      this.getLocation();
      setInterval(this.getStats, 1000 * 10);
      setInterval(this.updateMap, 1000 * 10);
      setInterval(this.count, 150);
      setInterval(this.getLocation, 1000 * 6);
    },

    methods: {
      selectCard(id) {
        this.selectedId = id;
        this.getSelectedToTop();
      },

      count() {
        var min = Math.ceil(0);
        var max = Math.floor(12);
        var myRandom = Math.floor(Math.random() * (max - min)) + min;
        this.iter += myRandom;
      },

      getLocation() {
        this.location = {
          lat: 37.786570, 
          lng: -122.402
        }
        // navigator.geolocation.getCurrentPosition(position => {
        //   this.location = {
        //     lat: position.coords.latitude,
        //     lng: position.coords.longitude
        //   }
        // });
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
              ["solved by police", stats.data["solved by police"]]
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
          },
          select: 'lat lon upvoterCount downvoterCount commentCount reportingUser followerCount category message comments time privacy status',
          limit: 20,
          severity: true,
          currentTime: Date.now(),
          currLat: this.lastCenter.lat,
          currLon: this.lastCenter.lng,
          role: "police"
        })
        .then(locations => {
          this.reports = locations.data;
          this.getSelectedToTop();
          this.reportLocs = this.reports.map(report => ({ position: { lat: report.lat, lng: report.lon }, id: report._id }));
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
  h4 {
    text-align: center;
  }

  .md-elevation-2 {
    padding: 8px;
    margin-left: 8px;
    margin-right: 8px;
    margin-top: 4px;
    margin-bottom: 4px;
    display: block;
  }
</style>
