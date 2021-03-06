<template>
  <div>
    <div class="tile is-ancestor">
      <article class="tile is-child box">
        <form @submit.prevent="submit">
          <h1 class="title">添加返回模板</h1>
          <div class="block">
            <label class="label">模板名称</label>
            <p class="control has-icon has-icon-right">
              <input v-bind:class="{ 'is-danger': !verifications.name }" class="input" type="text"
                     placeholder="请输入您的模板名称" v-model="template.name" v-on:input="verifications.name=true">
              <span class="icon is-small" v-if="!verifications.name">
               <i class="fa fa-warning"></i>
              </span>
              <span class="help is-danger" v-if="!verifications.name">{{ errorMessage.name }}</span>
            </p>
            <label class="label">MIME 类型</label>
            <p class="control">
              <span class="select">
                <select v-model.trim="template.mimeType">
                  <option value=0>application/json</option>
                  <option value=1>text/plain</option>
                  <option value=2>image/jpeg</option>
                </select>
              </span>
            </p>
            <label class="label">备注</label>
            <p class="control">
              <textarea class="textarea" placeholder="请输入您的备注" v-model.trim="template.note"></textarea>
            </p>
            <json-editor ref="editor" :onChange="inputResponseJson" :json="editorJson" v-on:verifyJson="verifyJson"/>
            <span class="help is-danger" v-if="!verifications.responseJson">{{ errorMessage.responseJson }}</span>
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
  import qs from 'qs'
  import {request} from '../network.js'
  import * as notification from '../notification.js'
  import JsonEditor from '../components/JsonEditor'

  export default {
    components: {
      JsonEditor
    },

    props: {},

    data () {
      return {
        template: {
          name: '',
          mimeType: 0,
          note: '',
          responseJson: '{}'
        },
        verifications: {
          name: true,
          responseJson: true
        },
        errorMessage: {
          name: '',
          modal: '',
          responseJson: ''
        },
        editorJson: {}
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
        for (var prop in this.verifications) {
          if (this.isEmpty(this.template[prop])) {
            this.verifications[prop] = false
            this.errorMessage[prop] = '不能为空'
            callback(false)
            return
          }
        }
        // 同名校验
        request('/frontend/res_template/repeat_name_verification', {
          method: 'get',
          params: {
            name: this.template.name
          }
        }).then((data) => {
          var repeatability = data['repeatability']
          if (repeatability) {
            this.verifications.name = false
            this.errorMessage.name = '该名称的项目已经存在'
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
            var formData = qs.stringify(this.template)
            console.log(this.template)
            request('/frontend/res_template/create', {
              method: 'post',
              data: formData
            }).then((data) => {
              notification.toast({
                message: '创建成功',
                type: 'success',
                duration: 2000
              })
              var model = data['res_template']
              this.$router.push({path: '/template/detail/' + model.res_template_id})
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
        this.template.responseJson = JSON.stringify(newVal)
      },

      verifyJson (verification) {
        this.errorMessage.responseJson = '格式错误'
        this.verifications.responseJson = verification
      }
    }
  }
</script>

<style scoped>
  .right {
    float: right;
  }
</style>
