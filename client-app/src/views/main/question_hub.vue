<template>
  <div class="background_wrap"></div>
  <div class="top_panel">
    <span>
      <el-button type="success" @click="dialog_visible = true">
      创建问题组
    </el-button>
    </span>
    <span>
      <el-input
          v-model="search_content"
          style="width: 100%"
          placeholder="search for question_set"
          :prefix-icon="Search"
          @keyup.enter.native="search"
      />
    </span>
    <span>
      <el-button type="info" @click="get_my_sets">
        我的问题组
      </el-button>
    </span>

  </div>

  <el-dialog
      v-model="dialog_visible"
      title="创建问题组"
      width="30%"
      draggable
      :before-close="handle_close"
      center>
    <create_ques_group_form @change_visible="change_dialog_visible"></create_ques_group_form>
  </el-dialog>
  <el-row class="groups-container" v-if="begin_flag">
    <ques_group_card v-for="(item,index) in start_ques_sets.creator_list" :creator_name="item"
                     :set_name="start_ques_sets.name_list[index]"
                     :date="start_ques_sets.date_list[index]"
                     :introduction="start_ques_sets.introduction_list[index]">
    </ques_group_card>
  </el-row>
  <el-row class="groups-container" v-else>
    <ques_group_card v-for="(item,index) in new_ques_sets.creator_list" :creator_name="item"
                     :set_name="new_ques_sets.name_list[index]"
                     :date="new_ques_sets.date_list[index]"
                     :introduction="new_ques_sets.introduction_list[index]">
    </ques_group_card>
  </el-row>

</template>

<script>
import {ref} from "vue";
import Create_ques_group_form from "@/views/main/question_component/create_ques_group_form.vue";
import {ElMessageBox} from "element-plus";
import ques_group_card from "@/views/main/question_component/ques_group_card.vue";
import {fetch_all_visible_ques_set, fetch_my_ques_sets, fetch_search_res} from "@/views/main/api";
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
  data() {
    return {
      start_ques_sets: {},
      store: userStateStore(),
      flag: true,
    }
  },
  created() {
    if (this.flag) {
      fetch_all_visible_ques_set(this.store.getUserId).then(
          (data) => {
            this.start_ques_sets = data;
            this.flag = false;
          })
    }
  },

  setup() {
    const dialog_visible = ref(false)
    const search_content = ref("")
    const store = userStateStore()
    const new_ques_sets = ref(null)
    const begin_flag = ref(true)

    const change_dialog_visible = (flag) => {
      dialog_visible.value = flag
    }

    const search = (event) => {
      fetch_search_res(store.getUserId, search_content.value).then(
          (res) => {
            new_ques_sets.value = res;
            begin_flag.value = false;
          }
      )
    }

    const get_my_sets = () => {
      fetch_my_ques_sets(store.getUserId).then(
          (res) => {
            new_ques_sets.value = res;
            begin_flag.value = false;
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

    return {
      dialog_visible,
      handle_close,
      change_dialog_visible,
      search_content,
      search,
      new_ques_sets,
      begin_flag,
      get_my_sets
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

.top_panel span{
  padding-left: 5px;
}
</style>