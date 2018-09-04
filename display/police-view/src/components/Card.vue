<template>
  <div class="card-expansion">
    <md-card
      class="init-color"
      v-bind:class="{ 'change-color': locData._id === selectedId }"
    >
      <md-card-header>
        <div class="row-icons">
          <strong style="color:red;"> {{ locData.category }} </strong>
          <md-icon>location_on</md-icon> <span style="color:blue;"> {{ locData.distance.toFixed(0) }}m </span>
          <md-icon>warning</md-icon> <span style="color: orange;"> {{ locData.severity.toFixed(2) }} </span>
        </div>
        <div class="row-icons">
          <md-icon>thumb_up</md-icon> {{ locData.upvoterCount }}
          <md-icon>thumb_down</md-icon> {{ locData.downvoterCount }}
          <md-icon>chat_bubble</md-icon> {{ locData.commentCount }}
          <md-icon>add_circle</md-icon> {{ locData.followerCount }}
        </div>
      </md-card-header>

      <md-card-content>
        <strong style="color:green;">{{ "Reported by "}}</strong>
        {{ locData.reportingUser }}
        <br>
        <strong style="color:green;">{{ "Message "}}</strong>
        {{ locData.message }}
        <br>
        <strong style="color:green;">{{ "Case ID "}}</strong>
        {{ locData._id }}
        <br>
        <strong style="color:green;">{{ "Time Reported "}}</strong>
        {{ (new Date(locData.time)).toLocaleString("en-US", { year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric' }) }}
      </md-card-content>

      <md-card-expand>
        <md-card-actions
          class="init-color"
          v-bind:class="{ 'change-color': locData._id === selectedId }"
          md-alignment="space-between"
        >
          <md-field>
            <label for="selectCaseStatus">Case Status</label>
            <md-select
              id="selectCaseStatus"
              v-model="locData['status']"
              placeholder="Case Status"
              @md-selected="updateStatus(locData._id, 'status', $event)"
            >
              <md-option value="pending">Pending</md-option>
              <md-option value="in progress">In Progress</md-option>
              <md-option value="solved by police">Solved by Police</md-option>
              <md-option value="solved by public">Solved by Public</md-option>
            </md-select>
          </md-field>

          <md-field>
            <label for="selectPrivacyStatus">Privacy Status</label>
            <md-select
              id="selectPrivacyStatus"
              v-model="locData['privacy']"
              placeholder="Privacy Status"
              @md-selected="updateStatus(locData._id, 'privacy', $event)"
            >
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
            <comment
              :key="index"
              v-for="(comment, index) in locData.comments"
              :comment="comment"
            >
            </comment>
          </md-card-content>
        </md-card-expand-content>
      </md-card-expand>
    </md-card>
  </div>
</template>

<script>
  import axios from 'axios';
  import Comment from './Comment';

  export default {
    name: 'CardExpansion',

    components: {
      Comment
    },
    
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
      },
      selectedId: String
    },

    mounted() {
      this.updateStatus = (id, field, value) => {
        axios.post('https://gony0gqug0.execute-api.us-east-1.amazonaws.com/beta/update', {
          reportId: id,
          field: field,
          value: value
        });
      }
    },

    methods: {
      updateStatus: (id, field, value) => 0
    }
  }
</script>

<style lang="scss" scoped>
  @-webkit-keyframes change-color-animation {
    0%    { background-color: white; }  
    50%   { background-color: #82be70; } 
    100%  { background-color: white; }  
  }

  @keyframes change-color-animation {
    0%    { background-color: white; }  
    50%   { background-color: #82be70; } 
    100%  { background-color: white; }  
  }

  .change-color {
    -webkit-animation-name: change-color-animation; /* Safari 4.0 - 8.0 */
    -webkit-animation-duration: 0.7s; /* Safari 4.0 - 8.0 */
    animation-name: change-color-animation;
    animation-duration: 0.7s;
  }

  @-webkit-keyframes init-color-animation {
    0%    { background-color: white; }  
    50%   { background-color: #82be70; } 
    100%  { background-color: white; }  
  }

  /* Standard syntax */
  @keyframes init-color-animation {
    0%    { background-color: white; }  
    50%  { background-color: #82be70; } 
    100%   { background-color: white; }  
  }

  .init-color {
    -webkit-animation-name: init-color-animation; /* Safari 4.0 - 8.0 */
    -webkit-animation-duration: 0.5s; /* Safari 4.0 - 8.0 */
    animation-name: init-color-animation;
    animation-duration: 0.5s;
  }

  .md-card {
    margin-left: 8px;
    margin-right: 8px;
    margin-top: 4px;
    margin-bottom: 4px;
    display: block;
  }

  .md-field {
    width: 40%;
  }

  .md-card-header {
    font-size: 15px;
    text-align: center;
  }

  .md-card-content {
    padding-left: 24px;
    padding-right: 24px;
    padding-bottom: 0;
  }

  .md-card-actions {
    padding-left: 24px;
    padding-right: 16px;
  }

  .row-icons {
    padding-top: 5px;
    padding-bottom: 5px;
  }

  .md-icon {
    margin-left: 8px;
    margin-right: 6px;
  }
</style>