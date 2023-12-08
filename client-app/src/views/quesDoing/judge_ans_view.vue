<template>
  <div class="main_container" id="main_container">
    <div class="title center_class">
        <span style="height: 45px;margin-left: 10px;margin-top: 50px">
          {{ ques_set_name }}
        </span>
    </div>
    <div class="row_margin">
      <el-col :offset="6" class="sub_title">
        问题组简介
      </el-col>
      <el-col :offset="6" :span="12" class="sub_content">
        {{ introduction }}
      </el-col>
    </div>
    <div class="row_margin">
      <el-col :offset="6" class="sub_title">
        完成情况
      </el-col>
      <el-col :offset="6" :span="12">
        <el-table :data="statistic" style="width: 100%">
          <el-table-column prop="sum" label="汇总" align="center"/>
          <el-table-column v-if="statistic[0].op > 0" prop="op" label="选择" align="center"/>
          <el-table-column v-if="statistic[0].blank > 0" prop="blank" label="填空" align="center"/>
          <el-table-column v-if="statistic[0].qa > 0" prop="qa" label="问答" align="center"/>
          <el-table-column v-if="statistic[0].mix > 0" prop="mix" label="复合" align="center"/>
        </el-table>
      </el-col>
    </div>
    <div style="margin-top: 15px">
      <el-pagination
          v-model:current-page="currentPage"
          :page-size="page_size"
          :hide-on-single-page="true"
          layout="prev, pager, next, jumper"
          :total="questions.length"
          @current-change="handleCurrentChange"
      />
      <div v-for="(ques, index) in display_ques" style="margin-bottom: 25px">
        <div v-if="index !== 0" class="dashed-divider"></div>
        <ques_judge_display :ques="ques" :id="(currentPage - 1)* page_size + index"
                            :score="scores[(currentPage - 1)* page_size + index]"
                            :ans="ans[(currentPage - 1)* page_size + index]"
                            @update_score="update_score"/>
      </div>
    </div>
  </div>
</template>

<script>
import userStateStore from "@/store";
import {ref} from "vue";
import router from "@/router";
import Ques_judge_display from "@/views/quesDoing/ques_judge_display.vue";

export default {
  name: 'judge_ans_view',
  props: ["hit_scores", "questions", "ques_set_name", "introduction", "ans"],
  components: {
    Ques_judge_display
  },
  setup(props) {
    const statistic = ref([
      {
        sum: 0,
        op: 0,
        blank: 0,
        qa: 0,
        mix: 0,
      },
      {
        sum: 0.0,
        op: 0.0,
        blank: 0.0,
        qa: 0.0,
        mix: 0.0,
      },
      {
        sum: 0.0,
        op: 0.0,
        blank: 0.0,
        qa: 0.0,
        mix: 0.0,
      }
    ])
    const store = userStateStore()
    const page = ref(1)
    const display_ques = ref([])
    const currentPage = ref(1)
    const page_size = ref(10)
    const profile_photo = ref('')
    const photo_flag = ref(true)
    const sum_score = ref(0.0)
    const scores = ref([])

    const handlePageChange = (val) => {
      page.value = val;
      display_ques.value = props.questions.slice(page.value * page_size.value + 1, page_size.value)
    }

    const gen_statistic = () => {
      let op_true_score = 0.0
      let op_all_score = 0.0
      let op_true_sum = 0
      let op_all_sum = 0
      let blank_true_score = 0.0
      let blank_all_score = 0.0
      let blank_true_sum = 0
      let blank_all_sum = 0
      let qa_true_score = 0.0
      let qa_all_score = 0.0
      let qa_true_sum = 0
      let qa_all_sum = 0
      let mix_true_score = 0.0
      let mix_all_score = 0.0
      let mix_true_sum = 0
      let mix_all_sum = 0
      let true_score = 0.0
      let all_score = 0.0
      let true_sum = 0
      let all_sum = 0
      let delta = 1e-5
      for (let i = 0; i < props.questions.length; i++) {
        all_score = all_score + props.questions[i].score
        all_sum++
        if (props.questions[i].content.type === '选择') {
          op_all_score = op_all_score + props.questions[i].score
          op_all_sum++
          op_true_score = op_true_score + scores.value[i]
          true_score = true_score + scores.value[i]
          if (Math.abs(props.questions[i].score - scores.value[i]) < delta) {
            op_true_sum++
            true_sum++
          }
        } else if (props.questions[i].content.type === '填空') {
          blank_all_score = blank_all_score + props.questions[i].score
          blank_all_sum++
          blank_true_score = blank_true_score + scores.value[i]
          true_score = true_score + scores.value[i]
          if (Math.abs(props.questions[i].score - scores.value[i]) < delta) {
            blank_true_sum++
            true_sum++
          }
        } else if (props.questions[i].content.type === '问答') {
          qa_all_score = qa_all_score + props.questions[i].score
          qa_all_sum++
          qa_true_score = qa_true_score + scores.value[i]
          true_score = true_score + scores.value[i]
          if (Math.abs(props.questions[i].score - scores.value[i]) < delta) {
            qa_true_sum++
            true_sum++
          }
        } else {
          mix_all_score = mix_all_score + props.questions[i].score
          mix_all_sum++
          let score_sum = 0.0
          for (let j = 0; j < props.questions[i].content.sub_problem.length; j++) {
            score_sum = score_sum + scores.value[i][j]
          }
          mix_true_score = mix_true_score + score_sum
          true_score = true_score + score_sum
          if (Math.abs(props.questions[i].score - score_sum) < delta) {
            mix_true_sum++
            true_sum++
          }
        }
      }
      statistic.value[0].sum = all_sum
      statistic.value[1].sum = true_sum + "/" + all_sum
      statistic.value[2].sum = true_score + "/" + all_score
      statistic.value[0].op = op_all_sum
      statistic.value[1].op = op_true_sum + "/" + op_all_sum
      statistic.value[2].op = op_true_score + "/" + op_all_score
      statistic.value[0].blank = blank_all_sum
      statistic.value[1].blank = blank_true_sum + "/" + blank_all_sum
      statistic.value[2].blank = blank_true_score + "/" + blank_all_score
      statistic.value[0].qa = qa_all_sum
      statistic.value[1].qa = qa_true_sum + "/" + qa_all_sum
      statistic.value[2].qa = qa_true_score + "/" + qa_all_score
      statistic.value[0].mix = mix_all_sum
      statistic.value[1].mix = mix_true_sum + "/" + mix_all_sum
      statistic.value[2].mix = mix_true_score + "/" + mix_all_score
    }

    const init = () => {
      for (let i = 0; i < props.questions.length; i++) {
        if (props.questions[i].content.type === '问答') {
          scores.value.push(0.0)
        } else if (props.questions[i].content.type === '复合') {
          let temp_array = []
          for (let j = 0; j < props.questions[i].content.sub_problem.length; j++) {
            if (props.questions[i].content.sub_problem[j].type !== '问答') {
              temp_array.push(props.hit_scores[i][j].toFixed(1))
            } else {
              temp_array.push(0.0)
            }
          }
          scores.value.push(temp_array)
        } else {
          scores.value.push(props.hit_scores[i].toFixed(1))
        }
      }
      display_ques.value = props.questions.slice((page.value - 1) * page_size.value,
          (page.value - 1) * page_size.value + page_size.value)
      gen_statistic()
    }

    init()

    const update_score = (data) => {
      scores.value[data.id] = data.score.toFixed(1)
      gen_statistic()
    }

    const exit = () => {
      router.push('/question_hub')
    }

    return {
      store,
      handleCurrentChange: handlePageChange,
      display_ques,
      currentPage,
      page_size,
      profile_photo,
      photo_flag,
      sum_score,
      statistic,
      exit,
      scores,
      update_score
    }
  }
}
</script>

<style scoped>
.main_container {
  left: 5%;
  width: 90%;
}

@font-face {
  font-family: 'YouSheBiaoTiHei';
  src: url('src/assets/fonts/YouSheBiaoTiHei-2.ttf') format('truetype');
}

.title {
  font-family: "Microsoft YaHei";
  font-size: 30px;
  font-weight: bold;
  color: black;
  margin-top: 10px;
  margin-bottom: 10px;
}

.center_class {
  display: flex;
  justify-content: center;
  align-items: center;
}

.sub_title {
  font-size: 16px;
  margin-bottom: 10px;
}

.sub_content {
  font-size: 14px;
  color: dimgray;
}

.row_margin {
  margin-bottom: 10px;
}

.dashed-divider {
  border-top: 1px dashed grey;
  opacity: 50%;
  margin-bottom: 25px;
  width: 100%;
}
</style>