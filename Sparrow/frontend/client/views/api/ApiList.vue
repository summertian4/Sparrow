<template>
  <div id="ApiList">
    <div class="tile is-ancestor">
      <div class="tile is-parent">
        <article class="tile is-child box">
          <h4 class="title">{{ project.name }} </h4>
          <router-link class="right" :to="{ path: '/api/create'}">
            <button class="button is-primary">添加</button>
          </router-link>
          <table class="table">
            <thead>
            <tr>
              <th>请求类型</th>
              <th>请求名称</th>
              <th>请求 URL</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
            </thead>
            <tfoot>
            <tr>
              <th>请求类型</th>
              <th>请求名称</th>
              <th>请求 URL</th>
              <th>状态</th>
              <th>操作</th>
            </tr>
            </tfoot>
            <tbody>
            <tr v-for="api in project.apis" :key="index">
              <td>
                <div v-if="api.method == 'GET'">
                  <div class="button green is-active">
                    {{ api.method }}
                  </div>
                </div>
                <div v-else-if="api.method == 'POST'">
                  <div class="button blue is-active">
                    {{ api.method }}
                  </div>
                </div>
                <div v-else-if="api.method == 'PUT'">
                  <div class="button yellow is-active">
                    {{ api.method }}
                  </div>
                </div>
                <div v-else-if="api.method == 'DELETE'">
                  <div class="button red is-active">
                    {{ api.method }}
                  </div>
                </div>
              </td>
              <td>{{ api.name }}</td>
              <td>
                {{ api.path }}
              </td>
              <td>{{ api.status }}</td>
              <td class="is-icon">
                <p class="control has-addons">
                  <a class="button">
                    <span class="icon is-small">
                      <i class="fa fa-pencil"></i>
                    </span>
                  </a>
                  <a class="button">
                    <span class="icon is-small">
                      <i class="fa fa-eye"></i>
                    </span>
                  </a>
                  <a class="button">
                    <span class="icon is-small">
                      <i class="fa fa-trash"></i>
                    </span>
                  </a>
                </p>
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
  import axios from 'axios'

  export default {
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
