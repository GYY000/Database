<template>
  <div class="background_wrap"></div>
  <div class="top_panel">
    <span>
      <el-button type="success" @click="dialog_visible = true">
        创建用户组
      </el-button>
    </span>
    <span>
      <el-input
          v-model="search_content"
          style="width: 100%"
          placeholder="search for team"
          :prefix-icon="Search"
          @keyup.enter.native="search"
      />
    </span>
  </div>

  <el-dialog
      v-model="dialog_visible"
      title="创建用户组"
      width="30%"
      draggable
      :before-close="handle_close"
      center>
    <create_team_form @change_visible="change_dialog_visible" @refresh="refresh"></create_team_form>
  </el-dialog>
  <el-row class="groups-container" v-if="begin_flag">
    <team_card v-for="(item,index) in start_team_sets.creator_list" :creator_name="item"
               :group_name="start_team_sets.group_name_list[index]"
               :date="start_team_sets.date_list[index]"
               :introduction="start_team_sets.introduction_list[index]">
    </team_card>
  </el-row>
  <el-row class="groups-container" v-else>
    <team_card v-for="(item,index) in new_team_sets.creator_list" :creator_name="item"
               :group_name="new_team_sets.group_name_list[index]"
               :date="new_team_sets.date_list[index]"
               :introduction="new_team_sets.introduction_list[index]">
    </team_card>
  </el-row>
</template>

<script>
import {ref} from "vue";
import {ElMessageBox} from "element-plus";

import {
  fetch_all_teams,
  fetch_search_team_res
} from "@/views/main/api";

import userStateStore from "@/store";
import {Search} from "@element-plus/icons-vue";
import Create_team_form from "@/views/main/team_component/create_team_form.vue";
import team_card from "@/views/main/team_component/team_card.vue";
import Edit_team from "@/views/main/team_component/edit_team.vue";
import router from "@/router";

export default {
  name: "team_hub",
  computed: {
    Search() {
      return Search
    }
  },
  components: {Edit_team, Create_team_form, team_card},
  data() {
    return {
      start_team_sets: {},
      store: userStateStore(),
      flag: true,
    }
  },

  created() {
    if (this.flag) {
      fetch_all_teams().then(
          (data) => {
            this.start_team_sets = data;
            this.flag = false;
          })
    }
  },

  setup() {
    const dialog_visible = ref(false)
    const search_content = ref("")
    const store = userStateStore()
    const new_team_sets = ref(null)
    const begin_flag = ref(true)

    const change_dialog_visible = (flag) => {
      dialog_visible.value = flag
    }

    const search = (event) => {
      fetch_search_team_res(search_content.value).then(
          (res) => {
            new_team_sets.value = res;
            begin_flag.value = false;
          }
      )
    }

    const handle_close = (done) => {
      ElMessageBox.confirm('确定取消创建用户组吗')
          .then(() => {
            done();
          })
          .catch(() => {
            // catch error
          });
    };

    const refresh = () => {
      router.go(0)
    }

    return {
      dialog_visible,
      handle_close,
      change_dialog_visible,
      search_content,
      search,
      new_team_sets,
      begin_flag,
      refresh
    }
  }
}
</script>

<style scoped>
.groups-container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-around;
  width: 95%;
  left: 2.5%;
}

.background_wrap {
  background: #f2f2f2;
  opacity: 80%;
}

.top_panel {
  display: flex;
  flex-direction: row-reverse;
  width: auto;
}

.top_panel span {
  padding-left: 5px;
}
</style>