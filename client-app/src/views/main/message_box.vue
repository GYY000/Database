<template>

</template>

<script>
import userStateStore from "@/store";

export default {
  name: "message_box",
  props: ["applier_name_list", "team_name_list", "time_list", "id_list"],
  setup() {
    const store = userStateStore
    return {
      store
    }
  }
}
</script>

<style scoped>

</style>