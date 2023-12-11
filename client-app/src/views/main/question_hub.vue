<template>
  <div class="background_wrap"></div>
  <el-row style="margin-bottom: 20px">
    <el-col :span="4">
      <div style="font-size: 18px;color: dodgerblue;margin-bottom: 5px;font-weight: bold">
        Question Hub
      </div>
      <div style="font-size: 12px">问题广场</div>
    </el-col>
    <el-col :offset="6" :span="14" style="display: flex;justify-content: right;margin-top: 5px">
      <el-button type="primary" @click="get_all_sets">
        全部问题组
      </el-button>
      <el-button type="primary" @click="get_favourite_sets">
        我的收藏
      </el-button>
      <el-button type="info" @click="get_my_sets">
        我的问题组
      </el-button>
      <el-input
          v-model="search_content"
          style="width: 200px;margin-bottom: 10px;margin-left: 6px;margin-right: 6px"
          placeholder="search for question_set"
          :prefix-icon="Search"
          @keyup.enter.native="search"
      />
      <el-button type="success" @click="dialog_visible = true">
        创建问题组
      </el-button>
    </el-col>
  </el-row>

  <el-dialog
      v-model="dialog_visible"
      title="创建问题组"
      width="30%"
      draggable
      :before-close="handle_close"
      center>
    <create_ques_group_form @change_visible="change_dialog_visible" @refresh="refresh"></create_ques_group_form>
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
  
  <el-row class="groups-container">
    <ques_group_card style="margin-right: 12px" v-for="(item,index) in ques_sets.creator_list" :creator_name="item"
                     :qs_id="ques_sets.id_list[index]"
                     :set_name="ques_sets.name_list[index]"
                     :date="ques_sets.date_list[index]"
                     :introduction="ques_sets.introduction_list[index]"
                     :key="ques_sets.id_list[index]">
    </ques_group_card>
  </el-row>
</template>

<script>
import {ref} from "vue";
import Create_ques_group_form from "@/views/main/question_component/create_ques_group_form.vue";
import {ElMessageBox} from "element-plus";
import ques_group_card from "@/views/main/question_component/ques_group_card.vue";
import {fetch_all_visible_ques_set, fetch_favourite_sets, fetch_my_ques_sets, fetch_search_res} from "@/views/main/api";
import userStateStore from "@/store";
import {Search} from "@element-plus/icons-vue";

export default {
  name: "question_hub",
  computed: {
    Search() {
      return Search
    }
  },
  components: {Create_ques_group_form, ques_group_card},

  setup() {
    const dialog_visible = ref(false)
    const search_content = ref("")
    const store = userStateStore()
    const ques_sets = ref([])
    const isLoading = ref(true)

    const init = () => {
      fetch_all_visible_ques_set(store.getUserId).then(
          (data) => {
            ques_sets.value = data;
            isLoading.value = false;
          })
    }

    const get_all_sets = () => {
      fetch_all_visible_ques_set(store.getUserId).then(
          (data) => {
            ques_sets.value = data;
          })
    }

    init()

    const change_dialog_visible = (flag) => {
      dialog_visible.value = flag
    }

    const search = (event) => {
      fetch_search_res(store.getUserId, search_content.value).then(
          (res) => {
            ques_sets.value = res;
            console.log(res)
            console.log(ques_sets.value)
          }
      )
    }

    const get_my_sets = () => {
      fetch_my_ques_sets(store.getUserId).then(
          (res) => {
            ques_sets.value = res
          }
      )
    }

    const get_favourite_sets = () => {
      fetch_favourite_sets(store.getUserId).then(
          (res) => {
            ques_sets.value = res
          }
      )
    }

    const handle_close = (done) => {
      ElMessageBox.confirm('确定取消创建问题组吗')
          .then(() => {
            done();
          })
          .catch(() => {
            // catch error
          });
    };

    const refresh = () => {
      router.go(0);
    }

    return {
      dialog_visible,
      handle_close,
      change_dialog_visible,
      search_content,
      search,
      ques_sets,
      get_my_sets,
      refresh,
      get_favourite_sets,
      get_all_sets,
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
  width: 100%;
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