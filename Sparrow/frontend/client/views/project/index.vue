<template>
  <div>
    <div class="tile is-ancestor">
      <router-link class="tile is-parent is-3" to="project/detail/0" v-for="project in projects" :key="index">
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
        projects: ''
      }
    },

    created () {
      this.loadProjects()
    },

    computed: {},

    methods: {
      loadProjects () {
        axios.get('/DataApis/data/project/list')
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
</style>
