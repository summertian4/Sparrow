<template>
  <div id="ApiList">
    <modal :visible="deleteModal.showModal" @close="close">
      <div class="box">
        <article>
          <div class="media-content">
            <div class="content">
              <p>
                <strong>确认删除 <strong class="is-danger">{{ currentApi.name }}</strong> ？</strong>
                <br/>
                如果您确定删除，请输入该项目的名称，防止误删除
              </p>
              <button class="button is-danger long" @click="deleteApi">确认删除</button>
            </div>
          </div>
        </article>
      </div>
    </modal>
    <div class="tile is-ancestor">
      <div class="tile is-parent">
        <article class="tile is-child box">
          <h4 class="title">{{ project.name }}</h4>
          <router-link class="right" :to="{ path: '/project/'+project.project_id+'/api/create'}">
            <button class="button is-primary">添加 </button>
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
            <tr v-for="api in apis" :key="api.api_id">
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
                  <a class="button" @click="jumpToAPIUpdate(api.api_id)">
                    <span class="icon is-small">
                      <i class="fa fa-pencil"></i>
                    </span>
                  </a>
                  <a class="button" @click="jumpToAPIDetail(api.api_id)">
                    <span class="icon is-small">
                      <i class="fa fa-eye"></i>
                    </span>
                  </a>
                  <a class="button" @click="deleteButtonClicked(api)">
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
  import {Modal} from 'vue-bulma-modal'
  import {request} from '../network.js'
  import * as notification from '../notification.js'

  export default {
    components: {
      Modal
    },
    props: {
      project: {
        project_id: '',
        name: '',
        status: 1,
        note: ''
      }
    },
    data () {
      return {
        apis: [],
        deleteModal: {
          showModal: false
        },
        currentApi: ''
      }
    },
    created () {
    },

    computed: {},

    methods: {
      close () {
        this.deleteModal.showModal = false
      },
      loadApis (projectId) {
        request('/frontend/project/' + projectId + '/api/list')
          .then((data) => {
            this.apis = data['apis']
          })
          .catch((data) => {
            notification.toast({
              message: data['message'],
              type: 'danger',
              duration: 2000
            })
          })
      },
      deleteButtonClicked (api) {
        this.deleteModal.showModal = true
        this.currentApi = api
      },
      deleteApi () {
        request('/frontend/project/' + this.project.project_id + '/api/delete/' + this.currentApi.api_id)
          .then((data) => {
            this.deleteModal.showModal = false
            notification.toast({
              message: '删除成功',
              type: 'success',
              duration: 2000
            })
            this.loadApis(this.project.project_id)
          })
          .catch((data) => {
            notification.toast({
              message: data['message'],
              type: 'danger',
              duration: 2000
            })
          })
      },
      jumpToAPIUpdate (apiId) {
        this.$router.push({path: '/project/' + this.project.project_id + '/api/update/' + apiId})
      },
      jumpToAPIDetail (apiId) {
        this.$router.push({path: '/project/' + this.project.project_id + '/api/detail/' + apiId})
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
