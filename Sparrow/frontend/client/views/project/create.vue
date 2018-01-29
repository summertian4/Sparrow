<template>
  <div>
    <modal :visible="showModal" @close="close">
      <div class="box">
        <article class="media">
          <div class="media-content">
            <div class="content">
              <p>
                <strong>创建失败</strong>
                <br>
                {{ errorMessage.modal }}
              </p>
            </div>
          </div>
        </article>
      </div>
    </modal>
    <div class="tile is-ancestor">
      <article class="tile is-child box">
        <form @submit.prevent="submit">
          <h1 class="title">添加项目</h1>
          <div class="block">
            <label class="label">项目名称</label>
            <p class="control has-icon has-icon-right">
              <input v-bind:class="{ 'is-danger': !verification.name }" class="input" type="text"
                     placeholder="请输入您的项目名称" v-model="project.name">
              <span class="icon is-small" v-if="!verification.name">
               <i class="fa fa-warning"></i>
              </span>
              <span class="help is-danger" v-if="!verification.name">{{ errorMessage.name }}</span>
            </p>
            <label class="label">备注</label>
            <p class="control">
              <textarea class="textarea" placeholder="请输入您的备注" v-model.trim="project.note"></textarea>
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
  import {Modal} from 'vue-bulma-modal'

  export default {
    components: {
      Modal
    },

    props: {},

    data () {
      return {
        showModal: false,
        project: {
          name: '',
          status: 1,
          note: ''
        },
        verification: {
          name: true
        },
        errorMessage: {
          name: '',
          modal: ''
        }
      }
    },

    created () {
    },

    computed: {},

    methods: {
      close () {
        this.$emit('close')
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
        for (var prop in this.verification) {
          if (this.isEmpty(this.project[prop])) {
            this.verification[prop] = false
            this.errorMessage[prop] = '不能为空'
            callback(false)
            return
          }
        }
        // 同名校验
        axios({
          method: 'get',
          url: '/frontend/project/search',
          params: {
            name: this.project.name
          }
        }).then((res) => {
          var repeatability = res.data['repeatability']
          if (repeatability) {
            this.verification.name = false
            this.errorMessage.name = '该名称的项目已经存在'
          }
          callback(!repeatability)
        }).catch(function (error) {
          console.log(error)
        })
      },

      submit () {
        this.verify((ok) => {
          if (ok) {
            var formData = qs.stringify(this.project)
            axios({
              method: 'post',
              url: '/frontend/project/create',
              data: formData
            }).then((res) => {
              var code = res.data['code']
              if (code === 200) {
                var model = res.data['project']
                this.$router.push({ path: '/project/detail/' + model.project_id })
              } else {
                this.errorMessage.modal = res.data['message']
                this.showModal = true
              }
            }).catch(function (error) {
              console.log(error)
            })
          }
        })
      }
    }
  }
</script>

<style scoped>
  .right {
    float: right;
  }
</style>
