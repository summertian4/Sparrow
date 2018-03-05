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
        <button class="right icon" v-on:click="starAPI">
          <i :class="{ 'fa-heart-o': !api.star, ' fa-heart': api.star }" class="fa"></i>
        </button>
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
            <label class="label">开启Mock</label>
          </div>
          <div class="control">
            <vb-switch type="primary" size="medium" v-model="mockStatus"></vb-switch>
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
  import VbSwitch from 'vue-bulma-switch'

  export default {
    components: {
      JsonEditor,
      Modal,
      VbSwitch
    },

    data () {
      return {
        api: {
          path: '',
          method: 'GET',
          name: '',
          status: 1,
          note: '',
          responseJson: '',
          star: false
        },
        deleteAPIModal: {
          showModal: false
        },
        mockStatus: true,
        shouldRequestUpdateStatus: false
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

    watch: {
      mockStatus: function (val) {
        if (val === true) {
          this.api.status = 1
        } else {
          this.api.status = 0
        }
        if (this.shouldRequestUpdateStatus === false) {
          this.shouldRequestUpdateStatus = true
        } else {
          this.updateStatus(this.api.status)
        }
      }
    },

    methods: {
      close () {
        this.deleteAPIModal.showModal = false
      },

      updateStatus (status) {
        request('/frontend/project/' + this.$route.params.project_id + '/api/' + this.$route.params.api_id + '/update_status', {
          method: 'get',
          params: {
            status: status
          }
        }).then((data) => {
          notification.toast({
            message: '更新 API 成功',
            type: 'success',
            duration: 2000
          })
        }).catch((data) => {
          notification.toast({
            message: data['message'],
            type: 'danger',
            duration: 2000
          })
        })
      },

      loadApi () {
        request('/frontend/project/' + this.$route.params.project_id + '/api/detail/' + this.$route.params.api_id, {
          method: 'get',
          params: {
            isOriginal: false
          }
        }).then((data) => {
          this.api = data['api']
          this.mockStatus = this.api.status === 1
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
      },

      starAPI () {
        request('/frontend/project/' + this.$route.params.project_id + '/api/star/' + this.$route.params.api_id, {
          method: 'get'
        }).then((data) => {
          var message = ''
          this.api.star = !this.api.star
          if (this.api.star === true) {
            message = '收藏成功'
          } else {
            message = '取消收藏成功'
          }
          notification.toast({
            message: message,
            type: 'success',
            duration: 2000
          })
        }).catch((data) => {
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

  .icon {
    outline: none;
    width: 45px;
    height: 45px;
    border: 0px;
    -webkit-tap-highlight-color: transparent;
  }
</style>
