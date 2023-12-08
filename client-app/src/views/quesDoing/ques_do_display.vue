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
    <el-checkbox-group v-model="option_ans" v-for="(item,index) in content.ops" size="small"
                       @change="update_ans">
      <el-row>
        <el-checkbox size="large" :label="String.fromCharCode(index + 65)"
                     style="width: 90%; margin-bottom: 10px" border>
          {{String.fromCharCode(index + 65) + '.' + item}}
        </el-checkbox>
      </el-row>
    </el-checkbox-group>
  </div>
  <div v-if="content.type === '填空'">
    <el-form style="margin-bottom: 10px;width: 80%" label-width="auto">
      <div v-for="(item,index) in blank_ans">
        <el-form-item :label="`空格 ${index + 1}`">
          <el-input v-model="blank_ans[index]" placeholder="请输入您的答案" @change="update_ans"></el-input>
        </el-form-item>
      </div>
    </el-form>
  </div>
  <div v-if="content.type === '复合'"
       style="display: flex;justify-content: left;width: 100%">
    <div style="width: 100%">
      <sub_problem_do v-for="(item, index) in content.sub_problem"
                      :sub_problem="item" :id="index"
                      @update_sub_ans="update_sub_ans"/>
    </div>
  </div>
  <div v-if="content.type === '问答'" style="margin-bottom: 10px">
    <mavon-editor :box-shadow="true" default-open="edit" :editable="true"
                  :toolbars-flag="true" :subfield="true"
                  style="min-width: 0px; width:70%;min-height: 400px"
                  placeholder="请输入您的答案"
                  @change="update_ans"
                  :value="q_and_a_ans" v-model="q_and_a_ans">
    </mavon-editor>
  </div>
</template>

<script>
import {ref} from "vue";
import Ques_option from "@/views/quesDoing/ques_option.vue";
import {DeleteFilled, Edit} from "@element-plus/icons-vue";
import Update_ques_form from "@/views/quesDoing/update_ques_form.vue";
import Sub_problem_show from "@/views/quesDoing/sub_problem_show.vue";
import Sub_problem_do from "@/views/quesDoing/sub_problem_do.vue";
import {array2String, string2Array} from "@/views/main/api";

export default {
  name: "ques_do_display",
  components: {Sub_problem_do, Sub_problem_show, Update_ques_form, Ques_option},
  props: ["ques", "id"],
  emits: ['update_ans'],

  setup(props, context) {
    const option_ans = ref([])
    const blank_ans = ref((props.ques.content.type === '填空') ?
        new Array(string2Array(props.ques.content.ans).length).fill('') : [])
    const sub_ans = ref()
    const q_and_a_ans = ref('')
    const filled_sub = ref([])

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

    const update_sub_ans = (data) => {
      sub_ans.value[data.id] = data.ans
      filled_sub.value[data.id] = data.filled
      update_ans()
    }

    const init = () => {
      if(props.ques.content.type === '复合') {
        sub_ans.value = []
        for(let ques1 of props.ques.content.sub_problem) {
          filled_sub.value.push(false)
          if(ques1.type === '填空') {
            sub_ans.value.push(new Array(string2Array(ques1.ans).length).fill(''))
          } else {
            sub_ans.value.push('')
          }
        }
      }
    }

    init()

    const update_ans = () => {
      let ans = null
      let filled = true
      if (props.ques.content.type === '选择') {
        ans = option_ans.value.join(',')
        filled = option_ans.value.length !== 0
      } else if (props.ques.content.type === '填空') {
        ans = blank_ans.value
        for(let i = 0;i < blank_ans.value.length;i++) {
          if(blank_ans.value[i] === '') {
            filled = false
          }
        }
      } else if (props.ques.content.type === '问答') {
        ans = q_and_a_ans.value
        filled = q_and_a_ans.value !== ''
      } else {
        ans = sub_ans.value
        for(let i = 0;i < filled_sub.value.length;i++) {
          if(filled_sub.value[i] === false) {
            filled = false
          }
        }
      }
      context.emit("update_ans", {id: props.id, ans: ans, filled: filled})
    }

    const serial_num = ref(props.ques.serial_num)
    const score = ref(props.ques.score)

    return {
      content,
      serial_num,
      score,
      option_ans,
      blank_ans,
      q_and_a_ans,
      update_sub_ans,
      update_ans
    }
  }
}
</script>

<style scoped>
</style>