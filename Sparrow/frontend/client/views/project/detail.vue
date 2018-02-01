<template>
  <div>
    <article class="tile is-child box">
      <tabs animation="slide" :only-fade="false">
        <tab-pane label="API 列表" selected>
          <api-list ref="apilist" :project="project"></api-list>
        </tab-pane>
        <tab-pane label="项目设置">
          <project-setting :project="project"></project-setting>
        </tab-pane>
      </tabs>
    </article>
  </div>
</template>

<script>
  import ProjectSetting from './ProjectSetting'
  import ApiList from '../api/ApiList'
  import {Tabs, TabPane} from 'vue-bulma-tabs'
  import axios from 'axios'

  export default {
    components: {
      Tabs,
      TabPane,
      ApiList,
      ProjectSetting
    },

    data () {
      return {
        project: ''
      }
    },

    created () {
      this.loadProjects()
    },

    computed: {},

    methods: {
      loadProjects () {
        axios.get('/frontend/project/detail/' + this.$route.params.id)
          .then((res) => {
            this.project = res.data['project']
            this.$refs.apilist.loadApis(this.project.project_id)
          })
          .catch(function (error) {
            console.log(error)
          })
      }
    }
  }
</script>

<style scoped>
  .button {
    width: 80px;
  }

  .green {
    background-color: #5eceb3;
    border-color: transparent;
    color: #fff;
  }

  .blue {
    background-color: #4373d5;
    border-color: transparent;
    color: #fff;
  }

  .yellow {
    background-color: #fadd6e;
    border-color: transparent;
    color: #fff;
  }

  .red {
    background-color: #eb4c64;
    border-color: transparent;
    color: #fff;
  }

  .right {
    float: right;
  }
</style>
