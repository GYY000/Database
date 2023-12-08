<template>
  <el-row style="margin-bottom: 5px">
    <el-col>
      <el-tag class="mx-1" size="large" v-if="content.type === '选择'">选择题</el-tag>
      <el-tag class="mx-1" size="large" v-if="content.type === '填空'">填空题</el-tag>
      <el-tag class="mx-1" size="large" v-if="content.type === '问答'">问答题</el-tag>
      <el-tag class="mx-1" size="large" v-if="content.type === '复合'">复合题型</el-tag>
      <el-tag class="mx-1" size="large" v-if="Math.abs(sum_score - ques.score) < delta" :type="'success'"
              style="margin-left: 10px">
        {{ sum_score.toFixed(1) }}/{{ ques.score.toFixed(1) }}分
      </el-tag>
      <el-tag class="mx-1" size="large" v-else-if="sum_score > delta" type="info" style="margin-left: 10px">
        {{ sum_score.toFixed(1) }}/{{ ques.score.toFixed(1) }}分
      </el-tag>
      <el-tag class="mx-1" size="large" v-else type="danger" style="margin-left: 10px">
        {{ sum_score.toFixed(1) }}/{{ ques.score.toFixed(1) }}分
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
      <div v-for="(item,index) in ans">
        <el-form-item :label="`空格 ${index + 1}`">
          <el-input v-model="ques_ans[index]" size="large"
                    v-if="sum_score === ques.score" placeholder="您的答案">
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
      <sub_problem_judge v-for="(item, index) in content.sub_problem"
                         :sub_problem="item" :id="index" :ans="ans[index]"
                         :score="cur_score[index]"
                         @update_sub_score="update_sub_score"/>
    </div>
  </div>
  <div v-if="content.type === '问答'" style="margin-bottom: 10px">
    <mavon-editor :box-shadow="true" default-open="preview" :editable="false"
                  :toolbars-flag="false" :subfield="false"
                  style="min-width: 0px; width:70%;min-height: 200px"
                  placeholder="您的答案为空"
                  :value="qa_ans" v-model="qa_ans">
    </mavon-editor>
    <el-row style="margin-top: 15px;margin-bottom: 15px;margin-left: 30px" align="center">
      <span style="font-size: 18px">评分</span>
      <el-input v-model="input_score" placeholder="评分"
              @change="update_score" style="margin-left: 30px;width: 30%"/>
    </el-row>
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

export default {
  name: "ques_judge_display",
  components: {Check, Close, Sub_problem_judge, Sub_problem_do, Sub_problem_show, Ques_option},
  props: ["ques", "id", "score", "ans"],
  emits: ['update_score'],

  setup(props, context) {
    const delta = ref(1e-7)
    const is_empty = ref()
    const sub_empty = ref([])
    const cur_score = ref(props.score)
    const input_score = ref('')
    const ques_ans = ref(props.ans)
    const sum_score = ref(0);
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
      if (props.ques.content.type === '问答') {
        is_empty.value = false
        sum_score.value = 0;
      } else if (props.ques.content.type === '复合') {
        is_empty.value = true
        sum_score.value = 0;
        for (let sub_ques of props.ques.content.sub_problem) {
          if (sub_ques.type === '问答') {
            is_empty.value = false
            sub_empty.value.push(false)
          } else {
            sub_empty.value.push(true)
          }
        }
        for (let i = 0; i < props.ques.content.sub_problem.length; i++) {
          sum_score.value = sum_score.value + cur_score.value[i];
        }
      } else {
        sum_score.value = cur_score.value
        is_empty.value = true
      }
    }

    init()

    const update_sub_score = (data) => {
      cur_score.value[data.id] = data.score
      sub_empty.value[data.id] = data.is_empty
      for (let i = 0; i < props.ques.content.sub_problem.length; i++) {
        sum_score.value = sum_score.value + cur_score.value[i];
      }
      update_score()
    }

    const update_score = () => {
      if (props.ques.content.type === '问答') {
        // TODO: 判断是否全是数字
        if (input_score.value !== '') {
          is_empty.value = true
          cur_score.value = parseFloat(input_score.value)
          if(cur_score.value > props.ques.score) {
            ElMessage.error("输入分数异常，请立即更正")
            cur_score.value = 0
            sum_score.value = 0
          } else {
            sum_score.value = cur_score.value
          }
        } else {
          is_empty.value = false
          cur_score.value = 0
          sum_score.value = 0
        }
      } else if (props.ques.content.type === '复合') {
        for (let temp of sub_empty.value) {
          if (temp === false) {
            is_empty.value = false
          }
        }
      }
      context.emit("update_score", {id: props.id, score: cur_score.value, is_empty: is_empty.value})
    }

    return {
      content,
      update_sub_score,
      update_score,
      input_score,
      check_color,
      ques_ans,
      sum_score,
      cur_score,
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