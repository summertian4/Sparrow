<template>
  <div>
    <modal :visible="deleteAPIModal.showModal" @close="close">
      <div class="box">
        <article>
          <div class="media-content">
            <div class="content">
              <p>
                <strong>删除该 API <strong class="is-danger">{{ api.name }}</strong> ？</strong>
              </p>
              <button class="button is-danger is-fullwidth" @click="deleteAPI">确认删除</button>
            </div>
          </div>
        </article>
      </div>
    </modal>
    <article class="tile is-child box">
      <h1 class="title">{{ api.path }}
        <a :href="mockLink" target="_blank">[MOCK]</a>
      </h1>
      <div class="block">
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">请求类型</label>
          </div>
          <div class="control is-grouped">
            {{ api.method }}
          </div>
        </div>
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">请求名称</label>
          </div>
          <div class="control">
            {{ api.name }}
          </div>
        </div>
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">是否启用</label>
          </div>
          <div class="control">
            {{ api.status }}
          </div>
        </div>
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">备注</label>
          </div>
          <div class="control">
            <textarea class="textarea" v-model="api.note" disabled></textarea>
          </div>
        </div>
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">请求参数</label>
          </div>
          <div class="control">
            <textarea class="textarea" disabled></textarea>
          </div>
        </div>
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">返回参数</label>
          </div>
          <div class="control">
            <json-editor class="jsoneditor" ref="editor" :json="api.responseJson" :editable="false"/>
          </div>
        </div>
        <div>
          <p class="control right">
            <button class="button is-primary" v-on:click="jumpToAPIUpdate">编辑</button>
          </p>
          <p class="control right">
            <button class="button is-danger" v-on:click="deleteAPIModal.showModal=true">删除</button>
          </p>
          <p class="blank">
          </p>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
  import {request} from '../network.js'
  import * as notification from '../notification.js'
  import JsonEditor from '../components/JsonEditor'
  import {Modal} from 'vue-bulma-modal'

  export default {
    components: {
      JsonEditor,
      Modal
    },

    data () {
      return {
        api: {
          path: '',
          method: 'GET',
          name: '',
          status: 1,
          note: '',
          responseJson: ''
        },
        deleteAPIModal: {
          showModal: false
        }
      }
    },

    created () {
      this.loadApi()
    },

    computed: {
      mockLink: function () {
        return 'http://' + window.location.host + '/mock/' + this.$route.params.project_id + '/' + this.api.path
      }
    },

    methods: {
      close () {
        this.deleteAPIModal.showModal = false
      },
      loadApi () {
        request('/frontend/project/' + this.$route.params.project_id + '/api/detail/' + this.$route.params.api_id, {
          method: 'get',
          params: {
            isOriginal: false
          }
        }).then((data) => {
          this.api = data['api']
        }).catch((data) => {
          notification.toast({
            message: data['message'],
            type: 'danger',
            duration: 2000
          })
        })
      },

      deleteAPI () {
        request('/frontend/project/' + this.$route.params.project_id + '/api/delete/' + this.$route.params.api_id)
          .then((data) => {
            this.deleteAPIModal.showModal = false
            notification.toast({
              message: '删除成功',
              type: 'success',
              duration: 2000
            })
            setTimeout(this.jumpToAPIList, 100)
          })
          .catch((data) => {
            notification.toast({
              message: data['message'],
              type: 'danger',
              duration: 2000
            })
          })
      },

      jumpToAPIUpdate () {
        this.$router.push({path: '/project/' + this.$route.params.project_id + '/api/update/' + this.$route.params.api_id})
      },

      jumpToAPIList () {
        this.$router.push({path: '/project/detail/' + this.$route.params.project_id})
      }
    }
  }
</script>

<style scoped>
  .title {
    font-weight: bold;
  }

  .blank {
    height: 30px;
  }

  .right {
    float: right;
  }

  .jsoneditor {
    width: 100%;
  }

  .button {
    width: 80px;
    margin-left: 10px;
  }
</style>
