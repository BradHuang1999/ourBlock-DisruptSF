<template>
  <div id='GBarGraph'>
    <GChart
      :settings="{packages: ['bar']}"    
      :data="chartData"
      :options="chartOptions"
      :createChart="(el, google) => new google.charts.Bar(el)"
      @ready="onChartReady"
    />
  </div>
</template>

<script>
import { GChart } from 'vue-google-charts'
export default {
  name: 'GBarGraph',
  components: {
    GChart
  },
  data () {
    return {
      chartsLib: null, 
      // Array will be automatically processed with visualization.arrayToDataTable function
      chartData: [
        ['Crime Type', 'Count', { role: "style" }],
        ['Larceny/Theft', 18792, 'color: gray'],
        ['Violence/Homicide', 6052, '#b87333'],
        ['Traffic Violations', 2316, '#b87333'],
        ['Drugs/Narcotics', 1580, '#b87333'],
        ['Kidnapping', 1337, '#b87333'],
        ['Sex Offences', 358, '#b87333'],
        ['Mental Health/Bullying', 155, '#b87333']
      ]
    }
  },
  computed: {
    chartOptions () {
      if (!this.chartsLib) return null
      return this.chartsLib.charts.Bar.convertOptions({
        bars: 'horizontal',
        height: 250,
        legend: {
          position: 'none'
        }
      })
    }
  },
  methods: {
    onChartReady (chart, google) {
      this.chartsLib = google
    }
  }
}
</script>

<style>
  #GBarGraph{
    height: 250px;
  }
</style>
