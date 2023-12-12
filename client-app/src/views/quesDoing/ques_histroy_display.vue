<template>
  <el-row style="margin-bottom: 5px">
    <el-col>
      <el-tag class="mx-1" size="large" v-if="content.type === '选择'">选择题</el-tag>
      <el-tag class="mx-1" size="large" v-if="content.type === '填空'">填空题</el-tag>
      <el-tag class="mx-1" size="large" v-if="content.type === '问答'">问答题</el-tag>
      <el-tag class="mx-1" size="large" v-if="content.type === '复合'">复合题型</el-tag>
      <el-tag class="mx-1" size="large" v-if="Math.abs(score - ques.score) < delta" :type="'success'"
              style="margin-left: 10px">
        {{ score.toFixed(1) }}/{{ ques.score.toFixed(1) }}分
      </el-tag>
      <el-tag class="mx-1" size="large" v-else-if="score > delta" type="info" style="margin-left: 10px">
        {{ score.toFixed(1) }}/{{ ques.score.toFixed(1) }}分
      </el-tag>
      <el-tag class="mx-1" size="large" v-else type="danger" style="margin-left: 10px">
        {{ score.toFixed(1) }}/{{ ques.score.toFixed(1) }}分
      </el-tag>
    </el-col>
  </el-row>
  <el-row style="font-weight: bold">
    <div style="width: 32px;display: inline-block">
      {{ id + 1 }}.
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
    <div v-for="(item,index) in content.ops">
      <el-row>
        <el-button v-if="check_color(index) === 'red'"
                   size="large" type="danger"
                   style="width: 90%; margin-bottom: 10px">
          <el-icon style="margin-right: 20px;height: 25px">
            <Close/>
          </el-icon>
          {{ String.fromCharCode(index + 65) + '.' + item }}
        </el-button>
        <el-button v-if="check_color(index) === 'yellow'"
                   size="large" type="warning"
                   style="width: 90%; margin-bottom: 10px">
          <el-icon style="margin-right: 20px;height: 25px">
            <Close/>
          </el-icon>
          {{ String.fromCharCode(index + 65) + '.' + item }}
        </el-button>
        <el-button v-if="check_color(index) === 'grey'" type="info"
                   size="large" style="width: 90%; margin-bottom: 10px">
          <span style="width: 30px"></span> {{ String.fromCharCode(index + 65) + '.' + item }}
        </el-button>
        <el-button v-if="check_color(index) === 'green'" type="success"
                   size="large" style="width: 90%; margin-bottom: 10px">
          <el-icon style="margin-right: 20px;height: 25px">
            <Check/>
          </el-icon>
          {{ String.fromCharCode(index + 65) + '.' + item }}
        </el-button>
      </el-row>
    </div>
  </div>
  <div v-if="content.type === '填空'">
    <el-form style="margin-bottom: 10px;width: 80%" label-width="auto">
      <div v-for="(item,index) in ques_ans">
        <el-form-item :label="`空格 ${index + 1}`">
          <el-input v-model="ques_ans[index]" size="large"
                    v-if="score === ques.score" placeholder="您的答案">
            <template #prefix>
              <el-icon style="color: green;height: 20px">
                <Select/>
              </el-icon>
            </template>
          </el-input>
          <el-input v-model="ques_ans[index]" size="large"
                    v-else placeholder="您的答案">
            <template #prefix>
              <el-icon style="color: red;height: 20px">
                <Close/>
              </el-icon>
            </template>
          </el-input>
          <el-input v-model="blank_ans[index]" size="large" placeholder="标准答案"
                    style="margin-top: 10px" disabled></el-input>
        </el-form-item>
      </div>
    </el-form>
  </div>
  <div v-if="content.type === '复合'"
       style="display: flex;justify-content: left;width: 100%">
    <div style="width: 100%">
      <sub_history_display v-for="(item, index) in content.sub_problem"
                         :sub_problem="item" :id="index" :ans="ques_ans[index]"/>
    </div>
  </div>
  <div v-if="content.type === '问答'" style="margin-bottom: 10px">
    <el-tag size="large" effect="dark" style="margin-bottom: 10px">您的答案</el-tag>
    <mavon-editor :box-shadow="true" default-open="preview" :editable="false"
                  :toolbars-flag="false" :subfield="false"
                  style="min-width: 0px; width:70%;min-height: 200px"
                  placeholder="您的答案为空"
                  :value="qa_ans" v-model="qa_ans">
    </mavon-editor>
    <el-tag size="large" effect="dark" style="margin-top: 10px;margin-bottom: 10px">标准答案</el-tag>
    <mavon-editor :box-shadow="true" default-open="preview" :editable="false"
                  :toolbars-flag="false" :subfield="false"
                  style="min-width: 0px; width:70%;min-height: 200px"
                  placeholder="标准答案"
                  :value="content.ans" v-model="content.ans">
    </mavon-editor>
  </div>
</template>

<script>
import {ref} from "vue";
import Ques_option from "@/views/quesDoing/ques_option.vue";
import Sub_problem_show from "@/views/quesDoing/sub_problem_show.vue";
import Sub_problem_do from "@/views/quesDoing/sub_problem_do.vue";
import Sub_problem_judge from "@/views/quesDoing/sub_problem_judge.vue";
import {Check, Close} from "@element-plus/icons-vue";
import {string2Array} from "@/views/main/api";
import {ElMessage} from "element-plus";
import Sub_history_display from "@/views/quesDoing/sub_history_display.vue";

export default {
  name: "ques_history_display",
  components: {Sub_history_display, Check, Close, Sub_problem_judge, Sub_problem_do, Sub_problem_show, Ques_option},
  props: ["ques", "id", "score", "ans"],

  setup(props) {
    const delta = ref(1e-7)
    const input_score = ref('')
    const ques_ans = ref('')
    const qa_ans = ref(props.ans)
    const option_ans = ref((props.ques.content.type === '选择') ?
        props.ques.content.ans.split(',') : [])
    const blank_ans = ref((props.ques.content.type === '填空') ?
        string2Array(props.ques.content.ans) : [])

    const check_color = (index) => {
      if ((props.ans.indexOf(String.fromCharCode(index + 65)) !== -1)
          && option_ans.value.indexOf(String.fromCharCode(index + 65)) !== -1) {
        return 'green'
      } else if ((props.ans.indexOf(String.fromCharCode(index + 65)) === -1)
          && option_ans.value.indexOf(String.fromCharCode(index + 65)) !== -1) {
        return 'yellow'
      } else if ((props.ans.indexOf(String.fromCharCode(index + 65)) !== -1)
          && option_ans.value.indexOf(String.fromCharCode(index + 65)) === -1) {
        return 'red'
      } else {
        return 'grey'
      }
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
      console.log(props.ans)
      ques_ans.value = props.ques.content.type === '选择' ? props.ans.split(',')
        : string2Array(props.ans)
    }

    init()
    return {
      content,
      input_score,
      check_color,
      ques_ans,
      option_ans,
      blank_ans,
      delta,
      qa_ans
    }
  }
}
</script>

<style scoped>
</style>