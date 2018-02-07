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
  import axios from 'axios'
  import {Modal} from 'vue-bulma-modal'
  import Notification from 'vue-bulma-notification'
  import Vue from 'vue'

  const NotificationComponent = Vue.extend(Notification)

  const openNotification = (propsData = {
    title: '',
    message: '',
    type: '',
    direction: '',
    duration: 4500,
    container: '.notifications'
  }) => {
    return new NotificationComponent({
      el: document.createElement('div'),
      propsData
    })
  }

  export default {
    components: {
      Modal,
      Notification
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
        axios.get('/frontend/project/' + projectId + '/api/list')
          .then((res) => {
            this.apis = res.data['apis']
          })
          .catch(function (error) {
            console.log(error)
          })
      },
      deleteButtonClicked (api) {
        this.deleteModal.showModal = true
        this.currentApi = api
      },
      deleteApi () {
        axios.get('/frontend/project/' + this.project.project_id + '/api/delete/' + this.currentApi.api_id)
          .then((res) => {
            var code = res.data['code']
            if (code === 200) {
              this.deleteModal.showModal = false
              openNotification({
                message: '删除成功',
                type: 'success',
                duration: 2000
              })
              this.loadApis(this.project.project_id)
              // reload
            } else {
              openNotification({
                message: '删除失败',
                type: 'danger',
                duration: 2000
              })
            }
          })
          .catch(function (error) {
            console.log(error)
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
