<template>
  <div class="card-expansion">
    <md-card>
      <md-card-header>
        <div style="text-align: center;">
          Homicide
          <md-icon>location_on</md-icon> 500m
          <md-icon>warning</md-icon> 74
        </div>
      </md-card-header>

      <md-card-content>
        <pre>{{ locData }}</pre>
      </md-card-content>

      <md-card-expand>
        <md-card-actions md-alignment="space-between">
          <md-field>
            <md-select v-model="status" placeholder="Case Status">
              <md-option value="pending">Pending</md-option>
              <md-option value="in progress">In Progress</md-option>
              <md-option value="solved by police">Solved by Police</md-option>
              <md-option value="solved by public">Solved by Public</md-option>
            </md-select>
          </md-field>

          <md-field>
            <md-select v-model="privacy" placeholder="Privacy Status">
              <md-option value="public">Public</md-option>
              <md-option value="private">Private</md-option>
            </md-select>
          </md-field>

          <md-card-expand-trigger>
            <md-button class="md-icon-button">
              <md-icon>keyboard_arrow_down</md-icon>
            </md-button>
          </md-card-expand-trigger>
        </md-card-actions>

        <md-card-expand-content>
          <md-card-content>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit. Optio itaque ea, nostrum odio. Dolores, sed
            accusantium quasi non, voluptas eius illo quas, saepe voluptate pariatur in deleniti minus sint. Excepturi.
          </md-card-content>
        </md-card-expand-content>
      </md-card-expand>
    </md-card>
  </div>
</template>

<script>
  export default {
    name: 'CardExpansion',
    props: {
      locData: {
        _id: String,
        lon: Number,
        lat: Number,
        upvoterCount: Number,
        downvoterCount: Number,
        followerCount: Number,
        category: String,
        time: Number,
        privacy: String,
        status: String
      }
    },
    data() {
      return {
        otherData: {
          lat: 22,
          lon: 23
        }
      }
    }
  }
</script>

<style lang="scss" scoped>
  .md-card {
    margin: 4px;
    display: inline-block;
    vertical-align: top;
  }
</style>