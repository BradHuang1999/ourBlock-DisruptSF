<template>
  <div class="md-layout md-gutter">
    <div class="md-layout-item md-size-25">
      <h1>ourBlock Logo</h1>
      <h2>Crimes by hour graph</h2>
      <h2>Crimes by category bar chart</h2>
      <h2>Reports from last 7 days</h2>
      <h2>Crimes by status pie chart</h2>
    </div>
    <div class="md-layout-item md-size-40">
      <Map />
    </div>
    <div class="md-layout-item md-size-35 md-scrollbar">
      <Card />
      <Card />
      <Card />
      <Card />
    </div>
  </div>
</template>

<script>
  import Card from './components/Card.vue'
  import Map from './components/Map.vue'

  export default {
    name: 'app',
    components: {
      Card, Map
    }
  }
</script>

<style>
  body, html{
    height: 100%;
    position: relative;
  }
</style>
