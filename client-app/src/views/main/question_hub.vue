<template>
  <div class="background_wrap"></div>
  <div class="top_panel">
    <el-button text @click="dialog_visible = true">
      创建问题组
    </el-button>
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
  <el-row class="groups-container">
    <ques_group_card v-for="(item,index) in ques_sets.creator_list" :creator_name="item"
                     :set_name="ques_sets.name_list[index]"
                     :avatar="ques_sets.avatar_list[index]" :date="ques_sets.date_list[index]"
                     :introduction="ques_sets.introduction_list[index]">
    </ques_group_card>
  </el-row>

</template>

<script>
import {ref} from "vue";
import Create_ques_group_form from "@/views/main/question_component/create_ques_group_form.vue";
import {ElMessageBox} from "element-plus";
import ques_group_card from "@/views/main/question_component/ques_group_card.vue";
import {fetch_all_visible_ques_set} from "@/views/main/api";
import userStateStore from "@/store";

export default {
  name: "question_hub",
  components: {Create_ques_group_form, ques_group_card},
  data() {
    return {
      ques_sets: {},
      store: userStateStore(),
    }
  },
  mounted() {
    fetch_all_visible_ques_set(this.store.getUserId).then(
        (data) => {
          this.ques_sets = data;
        })
  },

  setup() {
    const dialog_visible = ref(false)

    const change_dialog_visible = (flag) => {
      dialog_visible.value = flag
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
      change_dialog_visible
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
</style>