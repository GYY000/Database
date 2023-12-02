<template>
  <el-row style="margin-bottom: 5px">
    <el-col>
      <el-tag class="mx-1" size="large" v-if="content.type === '选择'">选择题</el-tag>
      <el-tag class="mx-1" size="large" v-if="content.type === '填空'">填空题</el-tag>
      <el-tag class="mx-1" size="large" v-if="content.type === '问答'">问答题</el-tag>
      <el-tag class="mx-1" size="large" v-if="content.type === '复合'">复合题型</el-tag>
      <el-tag class="mx-1" size="large" :type="'success'" style="margin-left: 10px">{{ score }}分</el-tag>
    </el-col>
  </el-row>
  <el-row style="font-weight: bold">
    <div style="width: 32px;display: inline-block">
      {{ ques.serial_num }}.
    </div>
    <span style="display:inline-block;">
      {{ content.name }}
    </span>
  </el-row>
  <el-row>
    <el-col :span="22">
      <v-md-preview :text="content.ques_content"></v-md-preview>
    </el-col>
  </el-row>
  <div v-if="content.type === '选择'">
    <el-checkbox-group v-model="ans" v-for="(item,index) in content.ops" size="small">
      <el-row>
        <el-checkbox size="large" :label="String.fromCharCode(index + 65) + '.' + item"
                     style="width: 90%; margin-bottom: 10px" border disabled/>
      </el-row>
    </el-checkbox-group>
    <el-form-item v-if="content.type === '选择'"
                  style="margin-bottom: 10px;width: 80%">
      <el-tag size="large" style="margin-right: 20px" effect="dark">答案</el-tag>
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
  <div v-if="content.type === '填空'">
    <div style="margin-bottom: 10px">
      <el-tag size="large" effect="dark">答案Demo</el-tag>
    </div>
    <el-form style="margin-bottom: 10px;width: 80%" label-width="auto">
      <div v-for="(item,index) in ans">
        <el-form-item :label="`空格 ${index + 1}`">
          <el-input :value="ans[index]" disabled></el-input>
        </el-form-item>
      </div>
    </el-form>
  </div>
  <div v-if="content.type === '复合'"
       style="display: flex;justify-content: left;width: 100%">
    <div style="width: 100%">
      <sub_problem_show v-for="(item, index) in content.sub_problem" :sub_problem="item" :id="index"/>
    </div>
  </div>
  <div v-if="content.type === '问答'" style="margin-bottom: 10px">
    <div style="margin-bottom: 10px">
      <el-tag size="large" effect="dark">答案Demo</el-tag>
    </div>
    <mavon-editor :box-shadow="true" :default-open="'preview'" :editable="false"
                  :toolbars-flag="false" :subfield="false" style="min-width: 0px; width:60%;min-height: 200px"
                  :value="content.ans" v-model="content.ans">
    </mavon-editor>
  </div>
  <el-row>
    <el-col>
      <el-button :icon="Edit" type="primary" @click="update_show = true" class="control_button">
        编辑
      </el-button>
      <el-button :icon="DeleteFilled" type="danger"
                 @click="delete_ques" style="margin-right: 50px">
        删除题目
      </el-button>
    </el-col>
  </el-row>

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
    const ans = ref((props.ques.content.type === '选择' || props.ques.content.type === '填空') ?
        props.ques.content.ans.split(',') : props.ques.content.ans)
    const update_show = ref(false)
    const option_answer = ref([''])

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

    const init = () => {
      console.log(content.value)
      console.log(ans.value)
    }

    init()

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
      ans,
      close_update_form,
      update_show,
      delete_ques,
      option_answer
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

.circle {
  width: 25px;
  height: 25px;
  border-radius: 50%;
  background-color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease;
  cursor: pointer;
}

.circle:hover {
  background-color: lightblue;
}

.letter {
  font-size: 15px;
}
</style>