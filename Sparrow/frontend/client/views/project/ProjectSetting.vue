<template>
  <article>
    <div>
      <modal :visible="updateModal.showModal" @close="close">
        <div class="box">
          <article class="media">
            <div class="media-content">
              <div class="content">
                <p>
                  <strong>创建失败</strong>
                  <br>
                  {{ updateModal.message }}
                </p>
              </div>
            </div>
          </article>
        </div>
      </modal>
      <modal :visible="deleteModal.showModal" @close="close">
        <div class="box">
          <article>
            <div class="media-content">
              <div class="content">
                <p>
                  <strong>确认删除 <strong class="is-danger">{{ project.name }}</strong> ？</strong>
                  <br/>
                  删除后该项目内的所有 API 将会被删除
                  <br/>
                  如果您确定删除，请输入该项目的名称，防止误删除
                </p>
                <input v-bind:class="{ 'is-danger': !deleteModalVerification }" class="input" type="text"
                       placeholder="请输入您的项目名称" v-model.trim="deleteModal.inputName">
                <hr class="gradient-red"/>
                <button class="button is-danger long" @click="deleteProject">确认删除</button>
              </div>
            </div>
          </article>
        </div>
      </modal>
      <div class="tile is-ancestor">
        <article class="tile is-child box">
          <form @submit.prevent="submit">
            <h1 class="title">更新基本信息</h1>
            <div class="block">
              <label class="label">项目名称</label>
              <p class="control has-icon has-icon-right">
                <input v-bind:class="{ 'is-danger': !verification.name }" class="input" type="text"
                       placeholder="请输入您的项目名称" v-model.trim="project.name">
                <span class="icon is-small" v-if="!verification.name">
               <i class="fa fa-warning"></i>
              </span>
                <span class="help is-danger" v-if="!verification.name" value="project.note">{{ errorMessage.name
                  }}</span>
              </p>
              <label class="label">备注</label>
              <p class="control">
                <textarea class="textarea" placeholder="请输入您的备注" v-model.trim="project.note"></textarea>
              </p>
              <div>
                <p class="control right">
                  <button class="button is-primary" type="submit">更新</button>
                </p>
                <p class="blank">
                </p>
              </div>
            </div>
          </form>
          <hr class="gradient-green"/>
          <button class="button is-danger long" v-on:click="deleteModal.showModal = true">删除</button>
        </article>
      </div>
    </div>
  </article>
</template>

<script>
  import axios from 'axios'
  import qs from 'qs'
  import {Modal} from 'vue-bulma-modal'
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
    components: {
      Modal,
      Notification
    },

    props: {
      project: {
        name: '',
        status: 1,
        note: ''
      }
    },

    data () {
      return {
        updateModal: {
          showModal: false,
          message: ''
        },
        deleteModal: {
          showModal: false,
          inputName: ''
        },
        newData: {
          name: '',
          status: 1,
          note: ''
        },
        verification: {
          name: true
        },
        errorMessage: {
          name: ''
        }
      }
    },

    created () {
    },

    computed: {
      deleteModalVerification: function () {
        return (this.deleteModal.inputName === this.project.name)
      }
    },

    methods: {
      close () {
        this.deleteModal.showModal = false
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
          var exist = res.data['exist']
          if (exist) {
            this.verification.name = false
            this.errorMessage.name = '该名称的项目已经存在'
          }
          callback(!exist)
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
              url: '/frontend/project/update/' + this.$route.params.id,
              data: formData
            }).then((res) => {
              var code = res.data['code']
              if (code === 200) {
                openNotification({
                  message: '更新成功',
                  type: 'success',
                  duration: 2000
                })
              } else {
                this.updateModal.message = res.data['message']
                this.updateModal.showModal = true
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
      },
      deleteProject () {
        if (this.deleteModalVerification === true) {
          axios({
            method: 'get',
            url: '/frontend/project/delete',
            params: {
              project_id: this.$route.params.id
            }
          }).then((res) => {
            var code = res.data['code']
            var message = res.data['message']
            if (code === 200) {
              this.close()
              openNotification({
                message: '删除成功',
                type: 'success',
                duration: 2000
              })
              setTimeout(this.jumpToProjectList, 100)
            } else {
              this.close()
              openNotification({
                message: message,
                type: 'failed',
                duration: 2000
              })
            }
          }).catch(function (error) {
            console.log(error)
          })
        }
      },
      jumpToProjectList () {
        this.$router.push({path: '/project'})
      }
    }
  }
</script>

<style scoped>
  .right {
    float: right;
  }

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

  strong.is-danger {
    color: #eb4c64;
  }

  .blank {
    height: 30px;
  }

  .long {
    width: 100%;
  }
</style>
