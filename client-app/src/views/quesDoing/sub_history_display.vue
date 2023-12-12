<template>
  <el-row style="margin-bottom: 5px;margin-left: 30px">
    <el-col>
      <el-tag class="mx-1" size="default" v-if="content.type === '选择'">选择题</el-tag>
      <el-tag class="mx-1" size="default" v-if="content.type === '填空'">填空题</el-tag>
      <el-tag class="mx-1" size="default" v-if="content.type === '问答'">问答题</el-tag>
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="22">
      <v-md-preview :text="content.ques_content"></v-md-preview>
    </el-col>
  </el-row>
  <div v-if="content.type === '选择'">
    <div v-for="(item,index) in content.ops">
      <el-row>
        <el-button v-if="check_color(index) === 'red'"
                   size="large" type="danger"
                   style="width: 90%; margin-bottom: 10px;margin-left: 30px">
          <el-icon style="margin-right: 20px;height: 25px">
            <Close/>
          </el-icon>
          {{ String.fromCharCode(index + 65) + '.' + item }}
        </el-button>
        <el-button v-if="check_color(index) === 'grey'"
                   size="large"
                   style="width: 90%; margin-bottom: 10px;margin-left: 30px">
          <span style="width: 30px"></span> {{ String.fromCharCode(index + 65) + '.' + item }}
        </el-button>
        <el-button v-if="check_color(index) === 'green'"
                   size="large"
                   type="success"
                   style="width: 90%; margin-bottom: 10px;margin-left: 30px">
          <el-icon style="margin-right: 20px;height: 25px">
            <Check/>
          </el-icon>
          {{ String.fromCharCode(index + 65) + '.' + item }}
        </el-button>
        <el-button v-if="check_color(index) === 'yellow'"
                   size="large"
                   type="warning"
                   style="width: 90%; margin-bottom: 10px;margin-left: 30px">
          <el-icon style="margin-right: 20px;height: 25px">
            <Close/>
          </el-icon>
          {{ String.fromCharCode(index + 65) + '.' + item }}
        </el-button>
      </el-row>
    </div>
  </div>
  <div v-if="content.type === '填空'">
    <el-form style="margin-bottom: 10px;width: 80%;margin-left: 30px" label-width="auto">
      <div v-for="(item,index) in ans">
        <el-form-item :label="`空格 ${index + 1}`">
          <el-input v-model="ans[index]" size="large"
                    placeholder="您的答案">
          </el-input>
          <el-input v-model="blank_ans[index]" size="large" style="margin-top: 10px"
                    placeholder="标准答案" disabled/>
        </el-form-item>
      </div>
    </el-form>
  </div>
  <div v-if="content.type === '问答'" style="margin-bottom: 10px">
    <el-tag size="large" effect="dark" style="margin-left: 30px;margin-bottom: 10px">您的答案</el-tag>
    <mavon-editor :box-shadow="true" default-open="preview" :editable="false"
                  :toolbars-flag="false" :subfield="false"
                  style="min-width: 0px; width:70%;min-height: 200px;margin-left: 30px"
                  placeholder="您的答案为空"
                  :value="qa_ans" v-model="qa_ans">
    </mavon-editor>
    <el-tag size="large" effect="dark" style="margin-left: 30px;margin-top: 10px;margin-bottom: 10px">标准答案</el-tag>
    <mavon-editor :box-shadow="true" default-open="preview" :editable="false"
                  :toolbars-flag="false" :subfield="false"
                  style="min-width: 0px; width:70%;min-height: 200px;margin-left: 30px"
                  placeholder="标准答案"
                  :value="content.ans" v-model="content.ans">
    </mavon-editor>
  </div>
</template>

<script>
import {ref} from "vue";
import Ques_option from "@/views/quesDoing/ques_option.vue";
import Update_ques_form from "@/views/quesDoing/update_ques_form.vue";
import Sub_problem_show from "@/views/quesDoing/sub_problem_show.vue";
import {string2Array} from "@/views/main/api";
import {Checked, Close} from "@element-plus/icons-vue";

export default {
  name: "sub_history_display",
  components: {Close, Checked, Sub_problem_show, Update_ques_form, Ques_option},
  props: ["sub_problem", "id", "ans"],

  setup(props) {
    const option_ans = ref((props.sub_problem.type === '选择') ?
        props.sub_problem.ans.split(',') : [])
    const blank_ans = ref((props.sub_problem.type === '填空') ?
        string2Array(props.sub_problem.ans) : [])
    const qa_ans = ref(props.ans)
    const delta = ref(1e-6)

    const content = ref(
        {
          ques_content: props.sub_problem.ques_content,
          type: props.sub_problem.type,
          ops: props.sub_problem.ops,
          ans: props.sub_problem.ans,
        }
    )

    const check_color = (index) => {
      if ((props.ans.indexOf(String.fromCharCode(index + 65)) !== -1)
          && option_ans.value.indexOf(String.fromCharCode(index + 65)) !== -1) {
        return 'green'
      } else if ((props.ans.indexOf(String.fromCharCode(index + 65)) !== -1)
          && option_ans.value.indexOf(String.fromCharCode(index + 65)) === -1) {
        return 'red'
      } else if ((props.ans.indexOf(String.fromCharCode(index + 65)) === -1)
          && option_ans.value.indexOf(String.fromCharCode(index + 65)) !== -1) {
        return 'yellow'
      } else {
        return 'grey'
      }
    }

    return {
      content,
      check_color,
      option_ans,
      blank_ans,
      qa_ans,
      delta
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