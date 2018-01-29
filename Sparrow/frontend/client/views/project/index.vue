<template>
  <div>
    <div class="bar">
      <router-link class="is-3" :to="{ path: '/project/create'}">
        <button class="button is-primary">添加</button>
      </router-link>
    </div>

    <div class="tile is-ancestor" v-for="(project, index) in projects" v-if="index % 4 === 0">
      <router-link class="tile is-parent is-3" :to="{ path: 'detail/'+projects[index].project_id}" append
                   v-if="index < projects.length">
        <article class="tile is-child box">
          <h4 class="title">{{ projects[index].name }}</h4>
          <div class="note">{{ projects[index].note }}</div>
        </article>
      </router-link>
      <router-link class="tile is-parent is-3" :to="{ path: 'detail/'+projects[index + 1].project_id}" append
                   v-if="index + 1 < projects.length">
        <article class="tile is-child box">
          <h4 class="title">{{ projects[index + 1].name }}</h4>
          <div class="note">{{ projects[index + 1].note }}</div>
        </article>
      </router-link>
      <router-link class="tile is-parent is-3" :to="{ path: 'detail/'+projects[index + 2].project_id}" append
                   v-if="index + 2 < projects.length">
        <article class="tile is-child box">
          <h4 class="title">{{ projects[index + 2].name }}</h4>
          <div class="note">{{ projects[index + 2].note }}</div>
        </article>
      </router-link>
      <router-link class="tile is-parent is-3" :to="{ path: 'detail/'+projects[index + 3].project_id}" append
                   v-if="index + 3 < projects.length">
        <article class="tile is-child box">
          <h4 class="title">{{ projects[index + 3].name }}</h4>
          <div class="note">{{ projects[index + 3].note }}</div>
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

  .note {
    height: 80px;
  }
</style>
