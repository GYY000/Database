<template>
  <img src="@/assets/image/background3.jpg" class="background">

</template>

<script>
import {ref} from "vue";
import {useRouter} from "vue-router";
import {fetch_all_member, fetch_all_team_ques_set} from "@/views/main/api";

export default {
  name: "manage_team",

  setup() {
    const qs_name_list = ref([])
    const qs_id_list = ref([])
    const qs_creator_list = ref([])
    const qs_date_list = ref([])
    const u_id_list = ref([])
    const u_name_list = ref([])
    const u_register_date_list = ref([])

    const init = () => {
      let router = useRouter()
      fetch_all_member(router.currentRoute.value.params.tid).then(
          (res) => {
            u_id_list.value = res.uid_list
            u_name_list.value = res.name_list
            u_register_date_list.value = res.register_date_list
          }
      )
      fetch_all_team_ques_set(router.currentRoute.value.params.tid).then(
          (res) => {
            qs_name_list.value = ref(res.name_list)
            qs_id_list.value = ref(res.qsid_list)
            qs_creator_list.value = ref(res.creator_list)
            qs_date_list.value = ref(res.date_list)
          }
      )
    }

    init()
    return {
      qs_name_list,
      qs_creator_list,
      qs_date_list,
      qs_id_list,
      u_id_list,
      u_name_list,
      u_register_date_list
    }
  }
}
</script>

<style scoped>
.background {
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  position: fixed;
  z-index: -1;
  opacity: 30%;
}
</style>