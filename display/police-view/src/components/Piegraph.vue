<template>
  <div id='app'>
  <GChart
    :settings="{packages: ['pie']}"    
    :data="chartData"
    :options="chartOptions"
    :createChart="(el, google) => new google.charts.Pie(el)"
    @ready="onChartReady"
  />
  </div>
</template>

<script>
import { GChart } from 'vue-google-charts'
export default {
  name: 'App',
  components: {
    GChart
  },
  data () {
    return {
      chartsLib: null, 
      // Array will be automatically processed with visualization.arrayToDataTable function
      chartData: [
        ['Status', 'Percentage'],
        ['Solved by Public', 2],
        ['Solved by Police', 3],
        ['Pending', 4],
        ['In progress', 2]
      ]
    }
  },
  computed: {
    chartOptions () {
      if (!this.chartsLib) return null
      return this.chartsLib.charts.Pie.convertOptions({
        chart: {
          title: 'Crime Status - PieGraph',
          subtitle: '2018 September 01'
        },
        //bars: 'horizontal', // Required for Material Bar Charts.
        //hAxis: { format: 'decimal' },
        //height: 400,
        //colors: ['#1b9e77', '#d95f02', '#7570b3']
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
