<template>
  <div>
    <article class="tile is-child box">
      <tabs animation="slide" :only-fade="false">
        <tab-pane label="API 列表" selected>
          <api-list></api-list>
        </tab-pane>
        <tab-pane label="项目设置">
          <project-setting></project-setting>
        </tab-pane>
        <tab-pane label="扫码登录">扫码登录</tab-pane>
      </tabs>
    </article>
  </div>
</template>

<script>
  import ProjectSetting from './ProjectSetting'
  import ApiList from '../api/ApiList'
  import {Tabs, TabPane} from 'vue-bulma-tabs'

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
    },

    computed: {},

    methods: {}
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
