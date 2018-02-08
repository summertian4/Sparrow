<template>
  <div>
    <div class="tile is-ancestor">
      <article class="tile is-child box">
        <form @submit.prevent="submit">
          <h1 class="title">添加 API</h1>
          <div class="block">
            <label class="label">请求路径</label>
            <p class="control has-icon has-icon-right">
              <input v-bind:class="{ 'is-danger': !verification.path }" class="input" type="text"
                     placeholder="输入您的 API 相对路径" v-model.trim="api.path">
              <span class="icon is-small" v-if="!verification.path">
               <i class="fa fa-warning"></i>
              </span>
              <span class="help is-danger" v-if="!verification.path">{{ errorMessage.path }}</span>
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
              <input v-bind:class="{ 'is-danger': !verification.name }" class="input" type="text"
                     placeholder="请求名称可以方便您快速找到 API" v-model="api.name">
              <span class="icon is-small" v-if="!verification.name">
               <i class="fa fa-warning"></i>
              </span>
              <span class="help is-danger" v-if="!verification.name">{{ errorMessage.name }}</span>
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
              <textarea v-bind:class="{ 'is-danger': !verification.responseJson }" class="textarea" placeholder=""
                        v-model.trim="api.responseJson"></textarea>
              <span class="icon is-small" v-if="!verification.responseJson">
               <i class="fa fa-warning"></i>
              </span>
              <span class="help is-danger" v-if="!verification.responseJson">{{ errorMessage.responseJson }}</span>
            </p>

            <p class="control">
              <button class="button is-primary right" type="submit">确认</button>
              <button class="button is-link right">取消</button>
            </p>
          </div>
        </form>
      </article>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import qs from 'qs'
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
    components: {},

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
        verification: {
          path: true,
          name: true,
          responseJson: true
        },
        errorMessage: {
          path: '',
          name: '',
          responseJson: ''
        }
      }
    },

    created () {
    },

    computed: {},

    methods: {
      isEmpty (obj) {
        if (obj.length === 0 || obj.length === '' || obj === null) {
          return true
        } else {
          return false
        }
      },
      verify (callback) {
        // 校验空串
        for (var prop in this.verification) {
          if (this.isEmpty(this.api[prop])) {
            this.verification[prop] = false
            this.errorMessage[prop] = '不能为空'
            callback(false)
            return
          }
        }
        // 同名校验
        axios({
          method: 'get',
          url: '/frontend/project/' + this.$route.params.project_id + '/api/search',
          params: {
            path: this.api.path
          }
        }).then((res) => {
          var repeatability = res.data['repeatability']
          if (repeatability) {
            this.verification.name = false
            this.errorMessage.name = '该请求路径的 API 已经存在'
          }
          callback(!repeatability)
        }).catch(function (error) {
          console.log(error)
          openNotification({
            message: error,
            type: 'danger',
            duration: 2000
          })
        })
      },

      submit () {
        this.verify((ok) => {
          if (ok) {
            var formData = qs.stringify(this.api)
            axios({
              method: 'post',
              url: '/frontend/project/' + this.$route.params.project_id + '/api/create',
              data: formData
            }).then((res) => {
              var code = res.data['code']
              if (code === 200) {
                var model = res.data['api']
                openNotification({
                  message: '创建成功',
                  type: 'success',
                  duration: 2000
                })
                this.$router.push({path: '/project/' + this.$route.params.project_id + '/api/detail/' + model.api_id})
              } else {
                this.errorMessage.modal = res.data['message']
                openNotification({
                  message: '创建失败',
                  type: 'danger',
                  duration: 2000
                })
              }
            }).catch(function (error) {
              console.log(error)
              openNotification({
                message: error,
                type: 'danger',
                duration: 2000
              })
            })
          }
        })
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
