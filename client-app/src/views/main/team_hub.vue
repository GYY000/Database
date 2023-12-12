<template>
  <div class="background_wrap"></div>
  <div class="top_panel">
    <span>
      <el-button type="success" @click="dialog_visible = true">
        创建团队
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
      title="创建团队"
      width="30%"
      draggable
      :before-close="handle_close"
      center>
    <create_team_form @change_visible="change_dialog_visible" @refresh="refresh"></create_team_form>
  </el-dialog>
  
  <div style="display: flex; justify-content: center; align-items: center" v-if="isLoading">
    <svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
      width="24px" height="30px" viewBox="0 0 24 30" style="enable-background:new 0 0 50 50;" xml:space="preserve">
      <rect x="0" y="13" width="4" height="5" fill="#333">
        <animate attributeName="height" attributeType="XML"
          values="5;21;5" 
          begin="0s" dur="0.6s" repeatCount="indefinite" />
        <animate attributeName="y" attributeType="XML"
          values="13; 5; 13"
          begin="0s" dur="0.6s" repeatCount="indefinite" />
      </rect>
      <rect x="10" y="13" width="4" height="5" fill="#333">
        <animate attributeName="height" attributeType="XML"
          values="5;21;5" 
          begin="0.15s" dur="0.6s" repeatCount="indefinite" />
        <animate attributeName="y" attributeType="XML"
          values="13; 5; 13"
          begin="0.15s" dur="0.6s" repeatCount="indefinite" />
      </rect>
      <rect x="20" y="13" width="4" height="5" fill="#333">
        <animate attributeName="height" attributeType="XML"
          values="5;21;5" 
          begin="0.3s" dur="0.6s" repeatCount="indefinite" />
        <animate attributeName="y" attributeType="XML"
          values="13; 5; 13"
          begin="0.3s" dur="0.6s" repeatCount="indefinite" />
      </rect>
    </svg>
    <span style="margin-left: 10px;">加载中...</span>
  </div>
  
  <el-row class="groups-container" v-if="begin_flag">
    <team_card v-for="(item,index) in team_sets.creator_list" :creator_name="item"
               :group_name="team_sets.group_name_list[index]"
               style="margin-right: 15px"
               :date="team_sets.date_list[index]"
               :tid="team_sets.tid_list[index]"
               :introduction="team_sets.introduction_list[index]">
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
import router from "@/router";

export default {
  name: "team_hub",
  computed: {
    Search() {
      return Search
    }
  },
  components: {Create_team_form, team_card},

  setup() {
    const dialog_visible = ref(false)
    const search_content = ref("")
    const store = userStateStore()
    const team_sets = ref(null)
    const begin_flag = ref(false)
    const isLoading = ref(true)

    const change_dialog_visible = (flag) => {
      dialog_visible.value = flag;
    }

    const init = () => {
      fetch_all_teams().then(
          (data) => {
            team_sets.value = data;
            begin_flag.value = true;
            isLoading.value = false;
          })
    }

    init()

    const search = (event) => {
      fetch_search_team_res(search_content.value).then(
          (res) => {
            team_sets.value = res;
            begin_flag.value = false;
          }
      )
    }

    const handle_close = (done) => {
      ElMessageBox.confirm('确定取消创建团队吗')
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
      team_sets,
      begin_flag,
      refresh,
      isLoading
    }
  }
}
</script>

<style scoped>
.groups-container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: left;
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