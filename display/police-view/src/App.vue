<template>
  <div class="md-layout max-100">
    <div class="md-layout-item md-size-25 max-100">
      <h1>ourBlock Logo</h1>
      <h2>Crimes by hour graph</h2>
      <h2>Crimes by category bar chart</h2>
      <h2>Reports from last 7 days</h2>
      <h2>Crimes by status pie chart</h2>
    </div>
    <div class="md-layout-item md-size-40 max-100">
      <Map />
    </div>
    <div class="md-layout-item md-size-35 md-scrollbar max-100">
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
  body, html, .max-100{
    height: 100%;
    width: 100%;
    overflow-x: visible;
  }
</style>
