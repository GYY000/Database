<template>
  <img src="@/assets/image/background3.jpg" class="background">
  <div class="secbackground"></div>
  <div class="center_class">
    <div class="main_container">
      <el-row>
        <el-col :span="2" v-if="creator_name === store.getUserName">
          <div style="font-size: 18px">
            {{team_name}}
          </div>
          <div>manage your team</div>
        </el-col>
        <el-col :span="2" v-else>
          <div style="font-size: 18px">
            {{team_name}}
          </div>
          <div>See what's going on</div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import {ref} from "vue";
import {useRouter} from "vue-router";
import {fetch_all_member, fetch_all_team_ques_set, fetch_team_info} from "@/views/main/api";
import Judge_ans_view from "@/views/quesDoing/judge_ans_view.vue";
import Ques_do_display from "@/views/quesDoing/ques_do_display.vue";
import userStateStore from "@/store";

export default {
  name: "manage_team",
  components: {Ques_do_display, Judge_ans_view},

  setup() {
    const qs_name_list = ref([])
    const qs_id_list = ref([])
    const qs_creator_list = ref([])
    const qs_date_list = ref([])
    const u_id_list = ref([])
    const u_name_list = ref([])
    const u_register_date_list = ref([])
    const creator_name = ref()
    const team_name = ref()
    const introduction = ref()
    const avatar = ref()
    const date = ref()
    const store = userStateStore

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
      fetch_team_info(router.currentRoute.value.params.tid).then(
          (res) => {
            creator_name.value = res.creator_name
            team_name.value = res.team_name
            introduction.value = res.introduction
            avatar.value = res.avatar.startsWith('/9j')
                ? 'data:image/jpg;base64,' + res.avatar : 'data:image/png;base64,' + res.avatar;
            date.value = res.date
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
      u_register_date_list,
      avatar,
      introduction,
      creator_name,
      date,
      team_name,
      store
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

.main_container {
  left: 5%;
  width: 90%;
}

.secbackground {
  top: 0;
  left: 2%;
  width: 96%;
  height: 100vh;
  position: fixed;
  z-index: -1;
  opacity: 100%;
  background-color: white;
}

.center_class {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>