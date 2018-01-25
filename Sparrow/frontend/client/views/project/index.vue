<template>
  <div>
    <div class="bar">
      <router-link class="is-3" :to="{ path: '/project/create'}">
        <button class="button is-primary">添加</button>
      </router-link>
    </div>

    <div class="tile is-ancestor">
      <router-link class="tile is-parent is-3" :to="{ path: 'detail/'+project.project_id}" append
                   v-for="project in projects" :key="project.project_id">
        <article class="tile is-child box">
          <h4 class="title">{{ project.name }}</h4>
          {{ project.note }}
        </article>
      </router-link>
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
        hello: 'hello',
        projects: ''
      }
    },

    created () {
      this.loadProjects()
    },

    computed: {},

    methods: {
      loadProjects () {
        axios.get('/frontend/project/list')
          .then((res) => {
            this.projects = res.data['projects']
          })
          .catch(function (error) {
            console.log(error)
          })
      }
    }
  }
</script>

<style scoped>
  .right {
    float: right;
  }

  .bar {
    margin-top: 20px;
    margin-bottom: 20px;
  }
</style>
