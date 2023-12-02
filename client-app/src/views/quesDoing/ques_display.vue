<template>
  <div>
    <el-row style="font-weight: bold; font-size: 20px;">
      <el-col :span="17">
        {{ ques.serial_num }}.
        {{ content.name }}
        <span style="font-weight: normal">
          ({{ score }}分)
        </span>
      </el-col>
      <el-col :span="7">
        <el-button :icon="Edit" type="primary" @click="update_show = true" class="control_button">
          编辑
        </el-button>
        <el-button :icon="DeleteFilled" type="danger"
                   @click="delete_ques" style="margin-right: 50px">
          删除题目
        </el-button>
      </el-col>
    </el-row>
    <div style="display: flex;justify-content: left">
      <v-md-preview :text="content.ques_content"></v-md-preview>
    </div>
    <div v-for="(item,index) in content.ops"
         style="display: flex;justify-content: left;width: 100%">
      <ques_option v-if="content.type === '选择'"
                   :index="index"
                   :content="item"
                   style="margin-left:30px; margin-bottom: 10px;width: 80%"></ques_option>
    </div>
    <div style="display: flex;justify-content: left;width: 100%">
      <el-form-item v-if="content.type === '选择'" style="margin-left:30px; margin-bottom: 10px;width: 80%">
        当前答案：
        <el-select
            v-model="ops_ans"
            multiple
            placeholder="正确答案"
            style="width: 240px"
            disabled
        >
          <el-option
              v-for="(item,index) in content.ops"
              :key="item"
              :label="String.fromCharCode(index + 65)"
              :value="String.fromCharCode(index + 65)"
          />
        </el-select>
      </el-form-item>
    </div>
    <div v-if="content.type === '填空'" style="display: flex;justify-content: left;width: 100%">
      <div style="margin-left:30px; margin-bottom: 10px;width: 80%">
        当前答案：
        <el-button text class="blank_ans">
          {{ content.ans }}
        </el-button>
      </div>
    </div>
    <div v-if="content.sub_problem.length !== 0"
         style="display: flex;justify-content: left;width: 100%">
      <div style="margin-left:30px; margin-bottom: 10px;width: 80%">
        <div>
          <sub_problem_show v-for="(item, index) in content.sub_problem" :sub_problem="item" :id="index"/>
        </div>
      </div>
    </div>
  </div>

  <el-dialog
      v-model="update_show"
      :show-close="true"
      center>
    <template #header="{ close, titleId}">
      <div class="edit-header">
        <div :id="titleId" class="edit_title">编辑问题</div>
      </div>
    </template>
    <update_ques_form @close_update_form="close_update_form" :ques="ques"/>
  </el-dialog>
</template>

<script>
import {ref} from "vue";
import {ElMessage} from "element-plus";
import {api_update_ques} from "@/views/main/api";
import Ques_option from "@/views/quesDoing/ques_option.vue";
import {DeleteFilled, Edit} from "@element-plus/icons-vue";
import Update_ques_form from "@/views/quesDoing/update_ques_form.vue";
import Sub_problem_show from "@/views/quesDoing/sub_problem_show.vue";

export default {
  name: "ques_display",
  computed: {
    Edit() {
      return Edit
    },
    DeleteFilled() {
      return DeleteFilled
    }
  },
  components: {Sub_problem_show, Update_ques_form, Ques_option},
  props: ["ques"],

  setup(props) {
    const ops_ans = ref((props.ques.content.type === '选择') ?
        props.ques.content.ans.split(',') : null)
    const update_show = ref(false)

    const close_update_form = () => {
      update_show.value = false;
    }

    const content = ref(
        {
          name: props.ques.content.name,
          ques_content: props.ques.content.ques_content,
          type: props.ques.content.type,
          ops: props.ques.content.ops,
          ans: props.ques.content.ans,
          sub_problem: props.ques.content.sub_problem
        }
    )
    const serial_num = ref(props.ques.serial_num)
    const score = ref(props.ques.score)

    const delete_ques = () => {
      let form1 = {
        is_delete: true,
        qid: props.ques.id,
      }
      api_update_ques(form1).then(
          (res) => {
            console.log(res)
            if (res.is_successful === "true") {
              ElMessage({
                message: "删除成功",
                type: "success",
              });
            } else {
              ElMessage({
                message: "删除失败",
                type: "error",
              });
            }
          }
      )
    }

    return {
      content,
      serial_num,
      score,
      ops_ans,
      close_update_form,
      update_show,
      delete_ques
    }
  }
}
</script>

<style scoped>

.edit_title {
  font-family: "Microsoft YaHei";
  font-weight: bold;
  font-size: 30px;
}

.blank_ans {
  width: 85%
}
</style>