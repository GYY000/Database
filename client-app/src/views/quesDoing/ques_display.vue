<template>
  <div>
    <div style="font-weight: bold; font-size: 20px; display: flex; align-items: center;
    justify-content: space-between;">
      <div>
        {{ ques.serial_num }}.
        {{ content.name }}
        <el-input v-model="score" v-if="edit_score"
                  @keyup.enter.native="update_score" class="score_updater"/>
        <el-button text @click="edit_score = true" v-else class="score_updater">
          {{ score }}
        </el-button>
        分
      </div>
      <el-button :icon="Edit" type="primary" @click="edit_ques" class="control_button">
        编辑
      </el-button>
      <el-button :icon="DeleteFilled" type="danger"
                 @click="update_ques(true)" style="margin-right: 50px">
        删除题目
      </el-button>
    </div>
    <div style="display: flex;justify-content: left">
      <v-md-preview :text="content.ques_content"></v-md-preview>
    </div>
    <div v-for="(item,index) in content.ops"
         style="display: flex;justify-content: left;width: 100%">
      <ques_option v-if="content.type === '选择'"
                   :index="index"
                   :content="item"
                   @delete_op="delete_op"
                   @upload_op="upload_op"
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
    </div>
    <div v-if="content.type === '填空'" style="display: flex;justify-content: left;width: 100%">
      <div style="margin-left:30px; margin-bottom: 10px;width: 80%">
        当前答案：
        <el-input v-model="content.ans" v-if="blank_ans_edit"
                  @keyup.enter.native="update_blank_ans"
                  clearable placeholder="请输入正确答案" class="blank_ans"/>
        <el-button text @click="blank_ans_edit = true" v-else class="blank_ans">
          {{ content.ans }}
        </el-button>
      </div>
    </div>
    <div v-if="content.sub_problem.length !== 0"
         style="display: flex;justify-content: left;width: 100%">
      <div style="margin-left:30px; margin-bottom: 10px;width: 80%">
        <div>
          subproblem:
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
    <update_ques_form @close="close_update_form" :ques="ques"/>
  </el-dialog>
</template>

<script>
import {ref} from "vue";
import {ElMessage} from "element-plus";
import {api_update_ques, upload_picture} from "@/views/main/api";
import Ques_option from "@/views/quesDoing/ques_option.vue";
import {DeleteFilled, Edit} from "@element-plus/icons-vue";
import Update_ques_form from "@/views/quesDoing/update_ques_form.vue";

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
  components: {Update_ques_form, Ques_option},
  props: ["ques"],

  setup(props, context) {
    const ops_ans = ref((props.ques.content.type === '选择') ?
        props.ques.content.ans.split(',') : null)
    const blank_ans = ref(props.ques.content.ans)
    const blank_ans_edit = ref(false)
    const content_edit = ref("preview")
    const tool_bar = ref(false)
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
    const edit_score = ref(false)

    const update_score = () => {
      edit_score.value = false
      update_ques(false)
    }

    const img_add = (pos, file) => {
      let form_data = new FormData
      form_data.append('image', file)
      upload_picture(form_data).then(
          (res) => {
            let ques_content = content.value.ques_content
            let name = file.name
            console.log(file.name)
            if (ques_content.includes(name)) {
              let oStr = `(${pos})`
              let nStr = `(${res.img_url})`
              let index = ques_content.indexOf(oStr)
              let str = ques_content.replace(oStr, '')
              let insertStr = (soure, start, newStr) => {
                return soure.slice(0, start) + newStr + soure.slice(start)
              }
              content.value.ques_content = insertStr(str, index, nStr)
            }
          }
      )
    }

    const update_ques = (is_delete) => {
      context.emit("upload_change", {'score': score.value, 'id': props.ques.id})
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
              console.log("suc")
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

    const update_blank_ans = () => {
      blank_ans_edit.value = false
      update_ques(false)
    }

    const sava_content = (value, render) => {
      tool_bar.value = false
      content.value.ques_content = value
      content_edit.value = "preview"
      update_ques(false)
    }

    const edit_ques = () => {
      update_show.value = true
    }

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
      update_blank_ans,
      content_edit,
      img_add,
      sava_content,
      tool_bar,
      edit_ques,
      close_update_form,
      update_show
    }
  }
}
</script>

<style scoped>

.score_updater {
  width: 8%;
  font-size: 20px;
}

.edit_title {
  font-family: "Microsoft YaHei";
  font-weight: bold;
  font-size: 30px;
}

.blank_ans {
  width: 85%
}
</style>