<template>
  <div>
    <article class="tile is-child box">
      <h1 class="title">{{ template.name }}
      </h1>
      <div class="block">
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">MIME 类型</label>
          </div>
          <div class="control is-grouped">
            {{ template.mimeType }}
          </div>
        </div>
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">返回参数</label>
          </div>
          <div class="control">
            <json-editor class="jsoneditor" ref="editor" :json="template.responseJson" :editable="false"/>
          </div>
        </div>
        <div class="control is-horizontal">
          <div class="control-label">
            <label class="label">备注</label>
          </div>
          <div class="control">
            <textarea class="textarea" v-model="template.note" disabled></textarea>
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
        template: {
          name: '',
          type: 0,
          note: '',
          responseJson: ''
        }
      }
    },

    created () {
      this.loadApi()
    },

    computed: {},

    methods: {
      loadApi () {
        request('/frontend/res_template/detail/' + this.$route.params.id, {
          method: 'get',
          params: {
            isOriginal: true
          }
        }).then((data) => {
          this.template = data['res_template']
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
