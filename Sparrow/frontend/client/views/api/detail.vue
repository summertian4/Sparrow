<template>
  <div>
    <article class="tile is-child box">
      <h1 class="title">{{ api.path }}</h1>
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
            <label class="label">请求名称</label>
          </div>
          <div class="control">
           {{ api.name }}
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
            <textarea class="textarea" v-model="api.responseJson" disabled></textarea>
          </div>
        </div>
      </div>
    </article>
  </div>
</template>

<script>
  import axios from 'axios'
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
        }
      }
    },

    created () {
      this.loadApi()
    },

    computed: {},

    methods: {
      loadApi () {
        axios({
          method: 'get',
          url: '/frontend/project/' + this.$route.params.project_id + '/api/detail/' + this.$route.params.api_id
        }).then((res) => {
          this.api = res.data['api']
        }).catch(function (error) {
          console.log(error)
          openNotification({
            message: error,
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
