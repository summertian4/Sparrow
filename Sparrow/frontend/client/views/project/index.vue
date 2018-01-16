<template>
  <div>
    <div class="tile is-ancestor">

      <router-link class="tile is-parent is-3" to="favorite">
        <article class="tile is-child box">
          <h4 class="title">Porject Name</h4>
          描述
          创建时间
          <a class="button is-primary">
            More
          </a>
        </article>
      </router-link>


      <div class="tile is-parent is-3">
        <article class="tile is-child box">
          <h4 class="title">Porject Name</h4>
          <table class="table is-narrow">
            <thead>
            <tr>
              <th>One</th>
              <th>Two</th>
            </tr>
            </thead>
            <tbody>
            <tr>
              <td>Three</td>
              <td>Four</td>
            </tr>
            <tr>
              <td>Five</td>
              <td>Six</td>
            </tr>
            </tbody>
          </table>
        </article>
      </div>
    </div>
  </div>
</template>

<script>
  import Chart from 'vue-bulma-chartjs'

  export default {
    components: {
      Chart
    },

    data () {
      return {}
    },

    computed: {},

    methods: {}
  }
</script>

<style scoped>
</style>
