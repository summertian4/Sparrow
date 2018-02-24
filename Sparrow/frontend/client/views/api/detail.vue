<template>
  <div>
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
      </div>
    </article>
  </div>
</template>

<script>
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
      }
    }
  }
</script>

<style scoped>
  hr.gradient-green {
    border: 0;
    height: 1px;
    background: #333;
    background-image: linear-gradient(to right, #ddd, #5eceb3, #ddd);
    margin-top: 40px;
    margin-bottom: 40px;
  }

  hr.gradient-red {
    border: 0;
    height: 1px;
    background: #333;
    background-image: linear-gradient(to right, #ddd, #eb4c64, #ddd);
    margin-top: 40px;
    margin-bottom: 40px;
  }

  .title {
    font-weight: bold;
  }

  .jsoneditor {
    width: 100%;
  }
</style>
