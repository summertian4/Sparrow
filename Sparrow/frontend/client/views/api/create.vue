<template>
  <div>
    <div class="tile is-ancestor">
      <article class="tile is-child box">
        <h1 class="title">添加 API</h1>
        <div class="block">
          <label class="label">请求路径</label>
          <p class="control">
            <input class="input" type="text" placeholder="输入您的 API 相对路径">
          </p>
          <label class="label">请求类型</label>
          <p class="control">
              <span class="select">
                <select>
                  <option>GET</option>
                  <option>POST</option>
                  <option>PUT</option>
                  <option>DELETE</option>
                </select>
              </span>
          </p>
          <label class="label">请求名称</label>
          <p class="control has-icon has-icon-right">
            <input class="input is-success" type="text" placeholder="请求名称可以方便您快速找到 API" value="bulma">
            <span class="icon is-small">
                <i class="fa fa-check"></i>
              </span>
            <span class="help is-success">This username is available</span>
          </p>
          <label class="label">是否启用</label>
          <p class="control">
              <span class="select">
                <select>
                  <option>是</option>
                  <option>否</option>
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
            <textarea class="textarea" placeholder="请输入您的备注"></textarea>
          </p>

          <label class="label">请求参数</label>
          <p class="control">
            <textarea class="textarea" placeholder=""></textarea>
          </p>

          <label class="label">返回数组</label>
          <p class="control">
            <textarea class="textarea" placeholder=""></textarea>
          </p>

          <p class="control">
            <button class="button is-primary right">确认</button>
            <button class="button is-link right">取消</button>
          </p>
        </div>
      </article>
    </div>
  </div>
</template>

<script>
  import Chart from 'vue-bulma-chartjs'
  import axios from 'axios'

  export default {
    components: {
      Chart
    },

    data () {
      return {
        project: ''
      }
    },

    created () {
      this.loadProjects()
    },

    computed: {},

    methods: {
      loadProjects () {
        axios.get('/DataApis/data/project/detail/' + this.$route.params.id)
          .then((res) => {
            this.project = res.data['project']
          })
          .catch(function (error) {
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
