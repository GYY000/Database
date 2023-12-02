<template>
  <div>
    <el-row style="font-weight: bold; font-size: 20px;">
      <el-col :span="17">
        <span style="font-weight: normal">
          [{{id}}].({{ content.score }}分)
        </span>
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
            v-model="ans"
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
          {{ ans }}
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import {ref} from "vue";
import {ElMessage} from "element-plus";
import {api_update_ques, upload_picture} from "@/views/main/api";
import Ques_option from "@/views/quesDoing/ques_option.vue";
import {DeleteFilled, Edit} from "@element-plus/icons-vue";
import Update_ques_form from "@/views/quesDoing/update_ques_form.vue";

export default {
  name: "sub_problem_show",
  computed: {
    Edit() {
      return Edit
    },
    DeleteFilled() {
      return DeleteFilled
    }
  },
  components: {Update_ques_form, Ques_option},
  props: ["sub_problem","id"],

  setup(props) {
    const ans = ref((props.sub_problem.type === '选择') ?
        props.sub_problem.ans.split(',') : props.sub_problem.ans)

    const content = ref(
        {
          ques_content: props.sub_problem.ques_content,
          type: props.sub_problem.type,
          ops: props.sub_problem.ops,
          score: props.sub_problem.score
        }
    )

    return {
      content,
      ans,
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