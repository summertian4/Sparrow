<template>
  <div>
    <div class="tile is-ancestor">
      <div class="tile is-parent">
        <article class="tile is-child box">
          <h4 class="title">收藏 API 列表</h4>
          <api-list :apis="apis"></api-list>
        </article>
      </div>
    </div>
  </div>
</template>

<script>
  import Chart from 'vue-bulma-chartjs'
  import ApiList from '../components/APIList'
  import {request} from '../network.js'
  import * as notification from '../notification.js'

  export default {
    components: {
      Chart,
      ApiList
    },

    data () {
      return {
        apis: []
      }
    },

    created () {
      this.loadFavoriteApis()
    },

    computed: {},

    methods: {
      loadFavoriteApis () {
        request('/frontend/favorite/list')
          .then((data) => {
            this.apis = data['apis']
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
</style>
