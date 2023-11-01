<template>
  <div>This is main page</div>
  <div>{{getUserName}}</div>
  <div>{{getProfilePhoto}}</div>
  <div>{{getRegDate}}</div>
  <button @click="logout">logout</button>
</template>

<style scoped>

</style>

<script>
export default {
  name: "index",
  computed: {
    getUserName() {
      return this.$store.getters.getUserName
    },
    getProfilePhoto() {
      return this.$store.getters.getProfilePhoto
    },
    getRegDate() {
      return this.$store.getters.getRegisterDate
    }
  },
  methods: {
    logout() {
      this.$store.dispatch("logout", {});
      this.$router.push({path: '/login'})
    }
  }
}
</script>