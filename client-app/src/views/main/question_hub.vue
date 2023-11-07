<template>
  <div>
    here is question_hub
  </div>
  <el-button text @click="dialog_visible = true">
    创建问题组
  </el-button>
  <el-dialog
      v-model="dialog_visible"
      title="创建问题组"
      width="30%"
      draggable
      :before-close="handle_close"
      center>
    <create_ques_group_form @change_visible="change_dialog_visible"></create_ques_group_form>
  </el-dialog>
</template>

<script>
import {ref} from "vue";
import Create_ques_group_form from "@/views/main/question_component/create_ques_group_form.vue";
import {ElMessageBox} from "element-plus";

export default {
  name: "question_hub",
  components: {Create_ques_group_form},
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

</style>