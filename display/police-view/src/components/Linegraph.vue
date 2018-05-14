<template>
  <div id='GLineGraph'>
  <GChart
    :settings="{packages: ['line']}"    
    :data="chartData"
    :options="options"
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

      chartData: [
        ['Time of Day', 'Drug/Narcotics', 'Kidnapping', 'Larceny/Theft', 'Mental Health/Bullying', 'Sex Offences', 'Traffic Violation', 'Violence/Homicide'],
        [0, 4800, 2541, 31665, 1290, 1739, 8404, 14298],
        [1, 3185, 1220, 21342, 320, 627, 5235, 11579],
        [2, 2612, 1064, 16735, 259, 627, 4249, 10537],
        [3, 1559, 657, 11653, 191, 425, 2560, 5792],
        [4, 1081, 464, 8494, 135, 236, 1801, 3820],
        [5, 536, 590, 7962, 208, 200, 1216, 3243],
        [6, 1459, 1209, 10377, 366, 188, 1453, 4703],
        [7, 3312, 3728, 15966, 464, 274, 3733, 6379],
        [8, 4341, 4562, 24752, 892, 547, 6163, 8940],
        [9, 5052, 3867, 26888, 891, 498, 6734, 9659],
        [10, 5703, 3899, 30473, 830, 500, 6342, 10414],
        [11, 6410, 3632, 32141, 703, 468, 6129, 11078],
        [12, 6705, 4854, 41857, 1374, 736, 7754, 13703],
        [13, 8469, 3629, 35483, 718, 519, 6512, 11938],
        [14, 9489, 3776, 37443, 656, 565, 6551, 12033],
        [15, 8896, 4350, 40784, 675, 689, 6556, 13474],
        [16, 9426, 3974, 43962, 653, 660, 8699, 13316],
        [17, 9898, 3791, 51501, 687, 679, 9266, 13514],
        [18, 8854, 3847, 59839, 706, 586, 8108, 13549],
        [19, 7591, 3217, 54442, 577, 549, 6876, 13111],
        [20, 5881, 3116, 49951, 546, 624, 5855, 12879],
        [21, 5653, 2962, 44796, 526, 574, 6031, 13302],
        [22, 6748, 2880, 44449, 429, 647, 8961, 13098],
        [23, 5877, 2478, 40156, 406, 669, 9407, 12371]
      ],

      options: {
        curveType: 'function',
        height: 180,
        legend: { position: 'none' },
        hAxis: { 
          titleTextStyle: { position: 'none' }, 
          position: 'none'
        }
      }
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
    height: 180px;
  }
</style>
