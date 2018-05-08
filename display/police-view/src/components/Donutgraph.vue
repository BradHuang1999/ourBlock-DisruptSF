<template>
  <div id='GDonutGraph'>
  <GChart
    :settings="{packages: ['corechart']}"    
    :data="chartData"
    :createChart="(el, google) => new google.visualization.PieChart(el)"
    :options="options"
    @ready="onChartReady"
  />
  </div>
</template>

<script>
import { GChart } from 'vue-google-charts'
export default {
  name: 'GPieGraph',

  props: ['pieData'],

  components: {
    GChart
  },

  data () {
    return {
      chartsLib: null,  
      // Array will be automatically processed with visualization.arrayToDataTable function
      chartData: [
        ['Classification', 'Incidents'],
        ['Larceny/Theft', 18792],
        ['Violence/Homicide', 6052],
        ['Traffic Violations', 2316],
        ['Drugs/Narcotics', 1580],
        ['Kidnapping', 1337],
        ['Sex Offences', 358],
        ['Mental Health/Bullying', 155]
      ],
      options: {
        pieHole: 0.25,
        height: 194,
        chartArea: {'width': '100%', 'height': '80%'}
      }
    }
  },
   /*computed: {
     chartOptions () {
       if (!this.chartsLib) return null
       console.log(this)
       console.log(this.chartsLib)
       console.log(this.chartsLib.visualization.PieChart.convertOptions)
       return this.chartsLib.charts.Pie.convertOptions({
         chart: {
           title: 'Crime Status - PieGraph',
         },
         legend: {
           position: 'none',    
         },
         options: {
           pieHole: 0.4,
         },
         //bars: 'horizontal', // Required for Material Bar Charts.
         //hAxis: { format: 'decimal' },
         //height: 400,
         //colors: ['#1b9e77', '#d95f02', '#7570b3']
       })
     }
   },*/

  methods: {
    onChartReady (chart, google) {
      this.chartsLib = google
    }
  }
}
</script>

<style>
  #GDonutGraph{
    height: 194px;
  }
</style>
