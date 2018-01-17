<template>
  <div>
    <div class="tile is-ancestor">
      <div class="tile is-parent">
        <article class="tile is-child box">
          <h4 class="title">{{ project.name }} {{ project.apis }}</h4>
          <table class="table">
            <thead>
            <tr>
              <th>请求类型</th>
              <th>请求名称</th>
              <th>请求 URL</th>
              <th>操作</th>
            </tr>
            </thead>
            <tfoot>
            <tr>
              <th>请求类型</th>
              <th>请求名称</th>
              <th>请求 URL</th>
              <th>操作</th>
            </tr>
            </tfoot>
            <tbody>
            <tr v-for="api in project.apis" :key="index">
              <td>
                <a class="button green is-active">{{ api.method }}</a>
              </td>
              <td>login</td>
              <td class="is-icon">
                登录
              </td>
              <td class="is-icon">
                <a href="#">
                  <i class="fa fa-edit"></i>
                </a>
              </td>
            </tr>
            <tr>
              <td>
                <a class="button green is-active">POST</a>
              </td>
              <td>login</td>
              <td class="is-icon">
                登录
              </td>
              <td class="is-icon">
                <a href="#">
                  <i class="fa fa-edit"></i>
                </a>
              </td>
            </tr>
            <tr>
              <td>
                <a class="button blue is-active">GET</a>
              </td>
              <td>login</td>
              <td class="is-icon">
                登录
              </td>
              <td class="is-icon">
                <a href="#">
                  <i class="fa fa-edit"></i>
                </a>
              </td>
            </tr>
            <tr>
              <td>
                <a class="button yellow is-active">PUT</a>
              </td>
              <td>login</td>
              <td class="is-icon">
                登录
              </td>
              <td class="is-icon">
                <a href="#">
                  <i class="fa fa-edit"></i>
                </a>
              </td>
            </tr>
            <tr>
              <td>
                <a class="button red is-active">DELETE</a>
              </td>
              <td>login</td>
              <td class="is-icon">
                登录
              </td>
              <td class="is-icon">
                <a href="#">
                  <i class="fa fa-edit"></i>
                </a>
              </td>
            </tr>
            </tbody>
          </table>
        </article>
      </div>
    </div>
  </div>
</template>

<script>
  import Chart from 'vue-bulma-chartjs'
  import axios from 'axios'

  export default {
    components: {
      Chart
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
        axios.get('/DataApis/data/project/detail/' + this.$route.params.id)
          .then((res) => {
            this.project = res.data['project']
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
</style>
