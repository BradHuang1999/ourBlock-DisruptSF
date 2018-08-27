<template>
  <div id='GLineGraph'>
  <GChart
    :settings="{packages: ['line']}"    
    :data="chartData"
    :options="chartOptions"
    :createChart="(el, google) => new google.charts.Line(el)"
    @ready="onChartReady"
  />
  </div>
</template>

<script>
import { GChart } from 'vue-google-charts'
export default {
  name: 'GLineGraph',

  components: {
    GChart
  },

  data () {
    return {
      chartsLib: null, 
      // Array will be automatically processed with visualization.arrayToDataTable function
      chartData: [
        ['Time of Day', 'Crimes in 2018'],
        [0 , 1300],
        [1 ,  855],
        [2 ,  661],
        [3 ,  517],
        [4 ,  363],
        [5 ,  362],
        [6 ,  429],
        [7 ,  628],
        [8 , 1026],
        [9 , 1130],
        [10, 1305],
        [11, 1457],
        [12, 1696],
        [13, 1494],
        [14, 1561],
        [15, 1631],
        [16, 1774],
        [17, 1870],
        [18, 2240],
        [19, 2128],
        [20, 1909],
        [21, 1582],
        [22, 1473],
        [23, 1199]
      ]
    }
  },
  computed: {
    chartOptions () {
      if (!this.chartsLib) return null
      return this.chartsLib.charts.Line.convertOptions({
        curveType: 'function',
        height: 220,
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
  #GLineGraph{
    height: 200px;
  }
</style>
