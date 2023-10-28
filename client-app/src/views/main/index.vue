<template>
  <div>This is main page</div>
  <div>{{getUserName}}</div>
</template>

<style scoped>

</style>

<script>
export default {
  name: "index",
  computed: {
    getUserName() {
      return this.$store.user_info.username
    }
  }

}
</script>