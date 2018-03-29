<template>
  <div>
    <article class="tile is-child box">
      <tabs animation="slide" :only-fade="false">
        <tab-pane label="API 列表" selected>
          <div>
            <h4 class="title left">{{ project.name }}</h4>
            <router-link class="right" :to="{ path: '/project/'+project.project_id+'/api/create'}">
              <button class="button is-primary">添加 </button>
            </router-link>
          </div>
          <api-list :apis="apisData.apis"></api-list>
          <div class="block right">
            <el-pagination
              layout="prev, pager, next"
              :page-size="apisData.limit"
              :total="apisData.total"
              @current-change="pageChange">
            </el-pagination>
          </div>
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
  import {Tabs, TabPane} from 'vue-bulma-tabs'
  import {request} from '../network.js'
  import * as notification from '../notification.js'
  import ApiList from '../components/APIList'
  import ElPagination from 'element-pagination'

  export default {
    components: {
      Tabs,
      TabPane,
      ApiList,
      ProjectSetting,
      ElPagination
    },

    data () {
      return {
        project: '',
        currentPage: 1,
        apisData: {}
      }
    },

    created () {
      this.loadProjects()
      this.loadApis()
    },

    computed: {},

    methods: {
      loadApis () {
        request('/frontend/project/' + this.$route.params.id + '/api/list', {
          params: {
            current_page: this.currentPage,
            limit: 10
          }
        })
          .then((data) => {
            this.apisData = data['apis_data']
          })
          .catch((data) => {
            notification.toast({
              message: data['message'],
              type: 'danger',
              duration: 2000
            })
          })
      },

      pageChange (currentPage) {
        this.currentPage = currentPage
        this.loadApis()
      },

      loadProjects () {
        request('/frontend/project/detail/' + this.$route.params.id)
          .then((data) => {
            this.project = data['project']
          })
          .catch((data) => {
            notification.toast({
              message: data['message'],
              type: 'danger',
              duration: 2000
            })
          })
      }
    }
  }
</script>

<style scoped>
  .right {
    display: inline-block;
    float: right;
  }

  .left {
    display: inline-block;
  }

  .button {
    width: 80px;
  }
</style>
