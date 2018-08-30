<template>
  <div id='app'>
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
  name: 'App',
  components: {
    GChart
  },
  data () {
    return {
      chartsLib: null, 
      // Array will be automatically processed with visualization.arrayToDataTable function
      chartData: [
        ['Crime Type', 'High Priority', 'Low Priority'],
        ['Larceny/Theft', 1000, 23],
        ['Violence/Homicide', 1170, 23],
        ['Kidnapping', 660, 435],
        ['Drugs/Narcotics', 1030, 12],
        ['Sex Offences', 1030, 234],
        ['Mental Health/Bullying', 1030, 1234],
        ['Traffic Violations', 1030, 232]
      ]
    }
  },
  computed: {
    chartOptions () {
      if (!this.chartsLib) return null
      return this.chartsLib.charts.Bar.convertOptions({
        chart: {
          title: 'Crimes by Category - BarGraph',
          subtitle: '2018 September 01'
        },
        bars: 'horizontal', // Required for Material Bar Charts.
        hAxis: { format: 'decimal' },
        height: 280,
        colors: ['#E43030', '#33FF33']
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
