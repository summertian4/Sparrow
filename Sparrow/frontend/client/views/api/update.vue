<template>
  <div>
    <div class="tile is-ancestor">
      <article class="tile is-child box">
        <form @submit.prevent="submit">
          <h1 class="title">更新 API</h1>
          <div class="block">
            <label class="label">请求路径</label>
            <p class="control has-icon has-icon-right">
              <input v-bind:class="{ 'is-danger': !verifications.path }" class="input" type="text"
                     placeholder="输入您的 API 相对路径" v-model.trim="api.path" v-on:input="verifications.path=true">
              <span class="icon is-small" v-if="!verifications.path">
               <i class="fa fa-warning"></i>
              </span>
              <span class="help is-danger" v-if="!verifications.path">{{ errorMessage.path }}</span>
            </p>
            <label class="label">请求类型</label>
            <p class="control">
              <span class="select">
                <select v-model.trim="api.method">
                  <option>GET</option>
                  <option>POST</option>
                  <option>PUT</option>
                  <option>DELETE</option>
                </select>
              </span>
            </p>
            <label class="label">请求名称</label>
            <p class="control has-icon has-icon-right">
              <input v-bind:class="{ 'is-danger': !verifications.name }" class="input" type="text"
                     placeholder="请求名称可以方便您快速找到 API" v-model="api.name" v-on:input="verifications.name=true">
              <span class="icon is-small" v-if="!verifications.name">
               <i class="fa fa-warning"></i>
              </span>
              <span class="help is-danger" v-if="!verifications.name">{{ errorMessage.name }}</span>
            </p>
            <label class="label">是否启用</label>
            <p class="control">
              <span class="select">
                <select v-model.trim="api.status">
                  <option value="1">是</option>
                  <option value="0">否</option>
                </select>
              </span>
            </p>

            <label class="label">备注</label>
            <p class="control">
              <textarea class="textarea" placeholder="请输入您的备注" v-model.trim="api.note"></textarea>
            </p>

            <label class="label">请求参数</label>
            <p class="control">
              <textarea class="textarea" placeholder=""></textarea>
            </p>

            <label class="label">返回数据</label>
            <p class="control  has-icon has-icon-right">
              <json-editor ref="editor" :onChange="inputResponseJson" :json="editorJson" v-on:verifyJson="verifyJson"/>
              <span class="help is-danger" v-if="!verifications.responseJson">{{ errorMessage.responseJson }}</span>
            </p>

            <p class="control">
              <button class="button is-primary right" type="submit">更新</button>
            </p>
          </div>
        </form>
      </article>
    </div>
  </div>
</template>

<script>
  import qs from 'qs'
  import {request} from '../network.js'
  import * as notification from '../notification.js'
  import JsonEditor from '../components/JsonEditor'

  export default {
    components: {
      JsonEditor
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
        verifications: {
          path: true,
          name: true,
          responseJson: true
        },
        errorMessage: {
          path: '',
          name: '',
          responseJson: ''
        },
        editorJson: {}
      }
    },

    created () {
      this.loadApi()
    },

    computed: {},

    methods: {
      loadApi () {
        request('/frontend/project/' + this.$route.params.project_id + '/api/detail/' + this.$route.params.api_id, {
          method: 'get'
        }).then((data) => {
          this.api = data['api']
          this.editorJson = JSON.parse(this.api.responseJson)
        }).catch((data) => {
          notification.toast({
            message: data['message'],
            type: 'danger',
            duration: 2000
          })
        })
      },

      isEmpty (obj) {
        if (obj.length === 0 || obj.length === '' || obj === null) {
          return true
        } else {
          return false
        }
      },
      verify (callback) {
        // 校验空串
        for (var prop in this.verifications) {
          if (this.isEmpty(this.api[prop])) {
            this.verifications[prop] = false
            this.errorMessage[prop] = '不能为空'
            callback(false)
            return
          }
        }

        // 同名校验
        request('/frontend/project/' + this.$route.params.project_id + '/api/repeat_name_verification', {
          method: 'get',
          params: {
            path: this.api.path,
            method: this.api.method,
            api_id: this.api.api_id
          }
        }).then((data) => {
          var repeatability = data['repeatability']
          if (repeatability) {
            this.verifications.path = false
            this.errorMessage.path = '该路径的 API 已经存在'
            callback(false)
          }
          var finalResult = true
          for (var value in this.verifications) {
            if (this.verifications[value] === false) {
              finalResult = false
            }
          }
          callback(finalResult)
        }).catch((data) => {
          notification.toast({
            message: data['message'],
            type: 'danger',
            duration: 2000
          })
        })
      },

      submit () {
        this.verify((ok) => {
          if (ok) {
            var formData = qs.stringify(this.api)
            request('/frontend/project/' + this.$route.params.project_id + '/api/update/' + this.$route.params.api_id, {
              method: 'post',
              data: formData
            }).then((data) => {
              notification.toast({
                message: '更新成功',
                type: 'success',
                duration: 2000
              })
              this.$router.push({path: '/project/' + this.$route.params.project_id + '/api/detail/' + this.$route.params.api_id})
            }).catch((data) => {
              notification.toast({
                message: data['message'],
                type: 'danger',
                duration: 2000
              })
            })
          }
        })
      },

      inputResponseJson (newVal) {
        this.api.responseJson = JSON.stringify(newVal)
      },

      verifyJson (verification) {
        this.errorMessage.responseJson = '格式错误'
        this.verifications.responseJson = verification
      }
    }
  }
</script>

<style scoped>
  .button {
    width: 80px;
  }

  .right {
    float: right;
  }
</style>
