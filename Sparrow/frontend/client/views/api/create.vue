<template>
  <div>
    <div class="tile is-ancestor">
      <article class="tile is-child box">
        <form @submit.prevent="submit">
          <h1 class="title">添加 API</h1>
          <div class="block">
            <label class="label">请求路径</label>
            <p class="control">
              <input class="input" type="text" placeholder="输入您的 API 相对路径" v-model.trim="api.path">
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
              <input class="input is-success" type="text" placeholder="请求名称可以方便您快速找到 API" v-model="api.name">
              <span class="icon is-small">
                <i class="fa fa-check"></i>
              </span>
              <span class="help is-success">This username is available</span>
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
            <!--<label class="label">Email</label>-->
            <!--<p class="control has-icon has-icon-right">-->
            <!--<input class="input is-danger" type="text" placeholder="Email input" value="hello@">-->
            <!--<span class="icon is-small">-->
            <!--<i class="fa fa-warning"></i>-->
            <!--</span>-->
            <!--<span class="help is-danger">This email is invalid</span>-->
            <!--</p>-->

            <label class="label">备注</label>
            <p class="control">
              <textarea class="textarea" placeholder="请输入您的备注" v-model.trim="api.note"></textarea>
            </p>

            <label class="label">请求参数</label>
            <p class="control">
              <textarea class="textarea" placeholder=""></textarea>
            </p>

            <label class="label">返回数据</label>
            <p class="control">
              <textarea class="textarea" placeholder="" v-model.trim="api.responseJson"></textarea>
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
  import Chart from 'vue-bulma-chartjs'
  import axios from 'axios'
  import qs from 'qs'

  export default {
    components: {
      Chart
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
          csrfmiddlewaretoken: this.$cookie.get('csrftoken')
        }
      }
    },

    created () {
    },

    computed: {},

    methods: {
      submit () {
        var formData = qs.stringify(this.api)
        axios({
          method: 'post',
          url: '/frontend/api/create',
          data: formData
        }).then(function (res) {
          console.log(res)
        }).catch(function (error) {
          console.log(error)
        })
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
