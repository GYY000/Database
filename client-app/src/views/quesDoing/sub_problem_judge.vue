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
  <div v-if="content.type === '选择'">
    <div v-for="(item,index) in content.ops">
      <el-row>
        <el-button v-if="check_color(index) === 'red'" type="danger"
                   style="width: 90%; margin-bottom: 10px">
          <el-icon>
            <Close/>
          </el-icon>
          {{ String.fromCharCode(index + 65) + '.' + item }}
        </el-button>
        <el-button v-if="check_color(index) === 'grey'"
                   style="width: 90%; margin-bottom: 10px">
          <span style="width: 30px"></span> {{ String.fromCharCode(index + 65) + '.' + item }}
        </el-button>
        <el-button v-if="check_color(index) === 'green'" type="success"
                   style="width: 90%; margin-bottom: 10px">
          <el-icon>
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
          <el-input v-model="ans[index]" placeholder="您的答案"></el-input>
          <el-input v-model="blank_ans[index]" placeholder="标准答案"></el-input>
        </el-form-item>
      </div>
    </el-form>
  </div>
  <div v-if="content.type === '问答'" style="margin-bottom: 10px">
    <mavon-editor :box-shadow="true" default-open="preview" :editable="false"
                  :toolbars-flag="false" :subfield="false"
                  style="min-width: 0px; width:70%;min-height: 400px"
                  placeholder="您的答案为空"
                  :value="ans">
    </mavon-editor>
    <el-input v-model="do_score" placeholder="请填入此题你的分数" @change="update_sub_score"></el-input>
    <mavon-editor :box-shadow="true" default-open="preview" :editable="false"
                  :toolbars-flag="false" :subfield="false"
                  style="min-width: 0px; width:70%;min-height: 400px"
                  placeholder="标准答案"
                  :value="content.ans">
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
  name: "sub_problem_judge",
  components: {Sub_problem_show, Update_ques_form, Ques_option},
  props: ["sub_problem", "id", "ans", "score"],
  emits: ['update_sub_score'],

  setup(props, context) {
    const do_score = ref('')
    const option_ans = ref((props.sub_problem.type === '选择') ?
          props.sub_problem.ans.split(',') : [])
    const blank_ans = ref((props.sub_problem.type === '填空') ?
        string2Array(props.sub_problem.ans) : [])

    const content = ref(
        {
          ques_content: props.sub_problem.ques_content,
          type: props.sub_problem.type,
          ops: props.sub_problem.ops,
          ans: props.sub_problem.ans,
        }
    )

    const update_sub_score = () => {
      let is_empty = true
      let score1 = 0
      if (props.sub_problem.type === '问答') {
        if (do_score.value === '') {
          score1 = 0
          is_empty = false
        } else {
          score1 = parseFloat(do_score.value)
        }
      } else {
        score1 = props.score
      }
      context.emit("update_sub_score", {id: props.id, score: score1, is_empty: is_empty})
    }

    const check_color = (index) => {
      if ((props.ans.indexOf(String.fromCharCode(index + 65)) !== -1)
          && option_ans.value.indexOf(String.fromCharCode(index + 65)) !== -1) {
        return 'green'
      } else if ((props.ans.indexOf(String.fromCharCode(index + 65)) !== -1)
          && option_ans.value.indexOf(String.fromCharCode(index + 65)) === -1) {
        return 'red'
      } else {
        return 'grey'
      }
    }

    return {
      content,
      update_sub_score,
      do_score,
      check_color,
      option_ans,
      blank_ans
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