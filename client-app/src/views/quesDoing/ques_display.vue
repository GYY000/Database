<template>
  <el-card shadow="never">
    <div style="display: flex;justify-content: left;width: 100%">
      <el-row>
        <el-col :span="4">
          <el-row>
            {{ ques.serial_num }}.
          </el-row>
          <el-row>
            <el-input v-model="score" v-if="edit_score"
                      @keyup.enter.native="update_score" class="score_updater"/>
            <el-button text @click="edit_score = true" v-else class="score_updater">
              {{ score }}
            </el-button>
          </el-row>
        </el-col>
        <el-col :span="20">
          <v-md-preview :text="content.ques_content"></v-md-preview>
          <el-row v-if="content.type === '选择'">
            <ques_option v-for="(item,index) in content.ops" :index="index" :content="item"
                         @delete_op="delete_op"
                         @upload_op="upload_op"
                         style="margin-bottom: 10px"></ques_option>
            <el-form-item v-if="content.type === '选择'">
              当前答案：
              <el-select
                  v-model="ops_ans"
                  multiple
                  placeholder="正确答案"
                  style="width: 240px"
                  @change="update_ques(false)"
              >
                <el-option
                    v-for="(item,index) in content.ops"
                    :key="item"
                    :label="String.fromCharCode(index + 65)"
                    :value="String.fromCharCode(index + 65)"
                />
              </el-select>
            </el-form-item>
          </el-row>
          <el-row v-if="content.type === '填空'">
            <el-col :span="8">当前答案：</el-col>
            <el-col :span="16">
              <el-input v-model="content.ans" v-if="blank_ans_edit"
                        @keyup.enter.native="update_blank_ans"
                        clearable placeholder="请输入正确答案" class="blank_ans"/>
              <el-button text @click="blank_ans_edit = true" v-else class="blank_ans">
                {{ content.ans }}
              </el-button>
            </el-col>
          </el-row>
          <div>
            subproblem:
          </div>
        </el-col>
      </el-row>
    </div>
  </el-card>
</template>

<script>
import {ref} from "vue";
import {ElMessage} from "element-plus";
import {api_update_ques} from "@/views/main/api";
import Ques_option from "@/views/quesDoing/ques_option.vue";

export default {
  name: "ques_display",
  components: {Ques_option},
  props: ["ques", "edit_mode"],

  setup(props, context) {
    const ops_ans = ref((props.ques.content.type === '选择') ?
        props.ques.content.ans.split(',') : null)
    const blank_ans = ref(props.ques.content.ans)
    const blank_ans_edit = ref(false)

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
    const edit_score = ref(false)

    const update_score = () => {
      edit_score.value = false
      update_ques(false)
    }

    const update_ques = (is_delete) => {
      content.value.ans =
          (content.value.type === '选择') ? ops_ans.value.join(',') : blank_ans.value;
      let form = {
        is_delete: is_delete,
        qid: props.ques.id,
        serial_num: serial_num.value,
        content: content.value,
        score: score.value
      }
      api_update_ques(form).then(
          (res) => {
            if (res.is_successful === "true") {
              ElMessage({
                message: "更新成功",
                type: "success",
              });
            } else {
              ElMessage({
                message: "更新失败",
                type: "error",
              });
            }
          }
      )
    }

    const delete_op = (index) => {
      content.value.ops.splice(index, 1)
      update_ques(false)
    }

    const upload_op = (data) => {
      content.value.ops[data.index] = data.option
      update_ques(false)
    }

    const init = () => {

    }

    const update_blank_ans = () => {
      blank_ans_edit.value = false
      update_ques(false)
    }

    init()

    return {
      update_ques,
      content,
      serial_num,
      score,
      update_score,
      edit_score,
      delete_op,
      upload_op,
      ops_ans,
      blank_ans,
      blank_ans_edit,
      update_blank_ans
    }
  }
}
</script>

<style scoped>
.score_updater {
  width: 15%
}

.blank_ans{
  width: 85%
}
</style>