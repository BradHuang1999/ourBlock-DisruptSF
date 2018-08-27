<template>
  <div id='GPieGraph'>
  <GChart
    :settings="{packages: ['corechart']}"    
    :data="chartData"
    :createChart="(el, google) => new google.visualization.PieChart(el)"
    @ready="onChartReady"
  />
  </div>
</template>

<script>
import { GChart } from 'vue-google-charts'
export default {
  name: 'GPieGraph',

  components: {
    GChart
  },

  data () {
    return {
      chartsLib: null, 
      // Array will be automatically processed with visualization.arrayToDataTable function
      chartData: [
        ['Status', 'Percentage'],
        ['Pending', 4],
        ['In progress', 2],
        ['Solved by Police', 3],
        ['Solved by Public', 2]
      ]
    }
  },
  // computed: {
  //   chartOptions () {
  //     if (!this.chartsLib) return null
  //     console.log(this)
  //     console.log(this.chartsLib)
  //     console.log(this.chartsLib.visualization.PieChart.convertOptions)
  //     return this.chartsLib.charts.Pie.convertOptions({
  //       chart: {
  //         title: 'Crime Status - PieGraph',
  //       },
  //       legend: {
  //         position: 'none'
  //       }
  //       //bars: 'horizontal', // Required for Material Bar Charts.
  //       //hAxis: { format: 'decimal' },
  //       //height: 400,
  //       //colors: ['#1b9e77', '#d95f02', '#7570b3']
  //     })
  //   }
  // },
  methods: {
    onChartReady (chart, google) {
      this.chartsLib = google
    }
  }
}
</script>

<style>
  #GPieGraph{
    height: 200px;
  }
</style>
