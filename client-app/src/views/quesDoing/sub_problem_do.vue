<template>
  <el-row style="margin-bottom: 5px;margin-left: 30px">
    <el-col>
      <el-tag class="mx-1" size="default" v-if="content.type === '选择'">选择题</el-tag>
      <el-tag class="mx-1" size="default" v-if="content.type === '填空'">填空题</el-tag>
      <el-tag class="mx-1" size="default" v-if="content.type === '问答'">问答题</el-tag>
      <el-tag class="mx-1" size="default" :type="'success'" style="margin-left: 10px">{{ sub_problem.score }}分</el-tag>
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="22">
      <v-md-preview :text="content.ques_content"></v-md-preview>
    </el-col>
  </el-row>
  <div v-if="content.type === '选择'" style="margin-bottom: 10px;margin-left: 30px">
    <el-checkbox-group v-model="option_ans" v-for="(item,index) in content.ops" size="small"
      @change="update_sub_ans">
      <el-row>
        <el-checkbox size="large" :label="String.fromCharCode(index + 65)"
                     style="width: 90%; margin-bottom: 10px" border>
          {{String.fromCharCode(index + 65) + '.' + item}}
        </el-checkbox>
      </el-row>
    </el-checkbox-group>
  </div>
  <div v-if="content.type === '填空'" style="margin-left: 30px">
    <el-form style="margin-bottom: 10px;width: 80%" label-width="auto">
      <div v-for="(item,index) in blank_ans">
        <el-form-item :label="`空格 ${index + 1}`">
          <el-input v-model="blank_ans[index]" placeholder="请输入您的答案"
                    @change="update_sub_ans"></el-input>
        </el-form-item>
      </div>
    </el-form>
  </div>
  <div v-if="content.type === '问答'" style="margin-bottom: 10px;margin-left: 30px">
    <mavon-editor :box-shadow="true" default-open="edit" :editable="true"
                  :toolbars-flag="true" :subfield="true"
                  style="min-width: 0px; width:70%;min-height: 400px"
                  placeholder="请输入您的答案"
                  @change="update_sub_ans"
                  :value="q_and_a_ans" v-model="q_and_a_ans">
    </mavon-editor>
  </div>
</template>

<script>
import {ref} from "vue";
import Ques_option from "@/views/quesDoing/ques_option.vue";
import Update_ques_form from "@/views/quesDoing/update_ques_form.vue";
import Sub_problem_show from "@/views/quesDoing/sub_problem_show.vue";
import {string2Array} from "@/views/main/api";

export default {
  name: "sub_problem_do",
  components: {Sub_problem_show, Update_ques_form, Ques_option},
  props: ["sub_problem", "id"],
  emits: ['update_sub_ans'],

  setup(props, context) {
    const option_ans = ref([])
    const blank_ans = ref((props.sub_problem.type === '填空') ?
        new Array(string2Array(props.sub_problem.ans).length).fill('') : [])
    const q_and_a_ans = ref('')

    const content = ref(
        {
          ques_content: props.sub_problem.ques_content,
          type: props.sub_problem.type,
          ops: props.sub_problem.ops,
          ans: props.sub_problem.ans,
        }
    )

    const update_sub_ans = () => {
      let ans = null
      let filled = true
      if(props.sub_problem.type === '选择') {
        ans = option_ans.value.join(',')
        filled = option_ans.value.length !== 0
      } else if(props.sub_problem.type === '填空') {
        ans = blank_ans.value
        for(let i = 0;i < blank_ans.value.length;i++) {
          if(blank_ans.value[i] === '') {
            filled = false
          }
        }
      } else if(props.sub_problem.type === '问答') {
        ans = q_and_a_ans.value
        filled = q_and_a_ans.value !== ''
      }
      context.emit("update_sub_ans", {id: props.id, ans: ans, filled: filled})
    }

    const score = ref(props.sub_problem.score)

    return {
      content,
      score,
      option_ans,
      blank_ans,
      q_and_a_ans,
      update_sub_ans
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