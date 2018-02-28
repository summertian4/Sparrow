<template>
  <div>
    <div class="bar">
      <router-link class="is-3" :to="{ path: '/template/create'}">
        <button class="button is-primary">添加</button>
      </router-link>
    </div>

    <div class="tile is-ancestor" v-for="(template, index) in templates" v-if="index % 3 === 0">
      <router-link class="tile is-parent is-4" :to="{ path: 'detail/'+templates[index].res_template_id}" append
                   v-if="index < templates.length">
        <article class="tile is-child box">
          <h4 class="title">{{ templates[index].name }}</h4>
          <div class="note">{{ templates[index].note }}</div>
        </article>
      </router-link>
      <router-link class="tile is-parent is-4" :to="{ path: 'detail/'+templates[index + 1].res_template_id}" append
                   v-if="index + 1 < templates.length">
        <article class="tile is-child box">
          <h4 class="title">{{ templates[index + 1].name }}</h4>
          <div class="note">{{ templates[index + 1].note }}</div>
        </article>
      </router-link>
      <router-link class="tile is-parent is-4" :to="{ path: 'detail/'+templates[index + 2].res_template_id}" append
                   v-if="index + 2 < templates.length">
        <article class="tile is-child box">
          <h4 class="title">{{ templates[index + 2].name }}</h4>
          <div class="note">{{ templates[index + 2].note }}</div>
        </article>
      </router-link>
    </div>
  </div>
</template>

<script>
  import {request} from '../network.js'
  import * as notification from '../notification.js'

  export default {
    components: {},

    data () {
      return {
        templates: ''
      }
    },

    created () {
      this.loadTemplates()
    },

    computed: {},

    methods: {
      loadTemplates () {
        request('/frontend/res_template/list')
          .then((data) => {
            this.templates = data['templates_data']['res_templates']
          })
          .catch((data) => {
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
  .bar {
    margin-top: 20px;
    margin-bottom: 20px;
  }

  .note {
    height: 80px;
  }
</style>
