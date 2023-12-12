<template>
  <img src="@/assets/image/background3.jpg" class="background">
  <div class="lower_panel" id="lower_panel">
    <el-row style="width: 100%" class="vertical-align-center">
      <el-col :span="3" style="height: 100%; margin-left: 30px;display: flex;align-items: center"
              @click="exit" class="hover_class">
        <el-icon style="width: 40px; height: 45px;margin-top: 12px">
          <ArrowLeft/>
        </el-icon>
        <div style="font-size: 16px;margin-top: 12px;display: inline-block">退出</div>
      </el-col>
      <el-col :span="8" :offset="7" style="height: 100%;font-size: 16px;color: #545455">
        {{ ques_set_name }}
      </el-col>
    </el-row>
  </div>
  <div class="secbackground"></div>
  <div class="center_class">
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
          <ques_history_display :ques="ques" :id="(currentPage - 1)* page_size + index"
                              :score="scores[(currentPage - 1)* page_size + index]"
                              :ans="ans[(currentPage - 1)* page_size + index]"/>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import userStateStore from "@/store";
import {onBeforeUnmount, ref} from "vue";
import router from "@/router";
import Ques_judge_display from "@/views/quesDoing/ques_judge_display.vue";
import {ElMessage} from "element-plus";
import {fetch_ques_history, hand_in_score} from "@/views/main/api";
import {useRouter} from "vue-router";
import Ques_history_display from "@/views/quesDoing/ques_histroy_display.vue";

export default {
  name: 'history_set',
  components: {
    Ques_history_display,
    Ques_judge_display
  },
  mounted() {
    const handleScroll = () => {
      let lower_panel = document.getElementById('lower_panel');
      let scrollDistance = window.pageYOffset || document.documentElement.scrollTop;
      let threshold = 20;

      if (scrollDistance < threshold || scrollDistance === 0) {
        lower_panel.style.top = '60px';
      } else {
        lower_panel.style.top = '0px';
      }
    };

    window.addEventListener('scroll', handleScroll);

    // 监听器添加后会在组件销毁时自动取消
    onBeforeUnmount(() => {
      window.removeEventListener('scroll', handleScroll);
    });
  },
  setup() {
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
    const hit_scores = ref([])
    const questions = ref([])
    const ques_set_name = ref('')
    const ans = ref([])
    const shid = ref()
    const introduction = ref('')

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
      for (let i = 0; i < questions.value.length; i++) {
        all_score = all_score + questions.value[i].score
        all_sum++
        if (questions.value[i].content.type === '选择') {
          op_all_score = op_all_score + questions.value[i].score
          op_all_sum++
          op_true_score = op_true_score + scores.value[i]
          true_score = true_score + scores.value[i]
          if (Math.abs(questions.value[i].score - scores.value[i]) < delta) {
            op_true_sum++
            true_sum++
          }
        } else if (questions.value[i].content.type === '填空') {
          blank_all_score = blank_all_score + questions.value[i].score
          blank_all_sum++
          blank_true_score = blank_true_score + scores.value[i]
          true_score = true_score + scores.value[i]
          if (Math.abs(questions.value[i].score - scores.value[i]) < delta) {
            blank_true_sum++
            true_sum++
          }
        } else if (questions.value[i].content.type === '问答') {
          qa_all_score = qa_all_score + questions.value[i].score
          qa_all_sum++
          qa_true_score = qa_true_score + scores.value[i]
          true_score = true_score + scores.value[i]
          if (Math.abs(questions.value[i].score - scores.value[i]) < delta) {
            qa_true_sum++
            true_sum++
          }
        } else {
          mix_all_score = mix_all_score + questions.value[i].score
          mix_all_sum++
          mix_true_score = mix_true_score + scores.value[i]
          true_score = true_score + scores.value[i]
          if (Math.abs(questions.value[i].score - scores.value[i]) < delta) {
            mix_true_sum++
            true_sum++
          }
        }
      }
      statistic.value[0].sum = all_sum
      statistic.value[1].sum = true_sum + "/" + all_sum
      statistic.value[2].sum = true_score.toFixed(1) + "/" + all_score.toFixed(1)
      statistic.value[0].op = op_all_sum
      statistic.value[1].op = op_true_sum + "/" + op_all_sum
      statistic.value[2].op = op_true_score.toFixed(1) + "/" + op_all_score.toFixed(1)
      statistic.value[0].blank = blank_all_sum
      statistic.value[1].blank = blank_true_sum + "/" + blank_all_sum
      statistic.value[2].blank = blank_true_score.toFixed(1) + "/" + blank_all_score.toFixed(1)
      statistic.value[0].qa = qa_all_sum
      statistic.value[1].qa = qa_true_sum + "/" + qa_all_sum
      statistic.value[2].qa = qa_true_score.toFixed(1) + "/" + qa_all_score.toFixed(1)
      statistic.value[0].mix = mix_all_sum
      statistic.value[1].mix = mix_true_sum + "/" + mix_all_sum
      statistic.value[2].mix = mix_true_score.toFixed(1) + "/" + mix_all_score.toFixed(1)
    }

    const init = () => {
      let router = useRouter()
      shid.value = router.currentRoute.value.params.shid
      fetch_ques_history(store.getUserId, shid.value).then(
          (res) => {
            hit_scores.value = res.get_score_list
            questions.value = res.question_list
            ques_set_name.value = res.ques_set_name
            introduction.value = res.introduction
            ans.value = res.ans_list
            scores.value = hit_scores.value
            display_ques.value = questions.value.slice((page.value - 1) * page_size.value,
                (page.value - 1) * page_size.value + page_size.value)
            gen_statistic()
          }
      )
    }

    init()

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
      hit_scores,
      ans,
      questions,
      ques_set_name,
      introduction
    }
  }
}
</script>

<style scoped>
.secbackground {
  top: 0;
  left: 2%;
  width: 96%;
  height: 100vh;
  position: fixed;
  z-index: -1;
  opacity: 100%;
  background-color: white;
}

.background {
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  position: fixed;
  z-index: -1;
  opacity: 30%;
}

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

.lower_panel {
  background: white;
  height: 70px;
  left: 0;
  top: 60px;
  width: 100%;
  position: fixed;
  z-index: 9999;
}

.vertical-align-center {
  display: flex;
  align-items: center;
}

.hover_class:hover {
  color: #545455;
  cursor: pointer;
}

.hover_class {
  color: #545455;
}

.right-panel1 {
  position: fixed;
  top: 50%;
  right: 1%;
  transform: translateY(-50%);
  height: 300px;
  width: 200px;
  background: white;
  box-shadow: 0 0 3px 2px rgba(0, 0, 0, 0.3);
  border-radius: 5%;
  overflow-y: scroll;
}

.right-panel2 {
  position: fixed;
  top: 27.4%;
  right: 1%;
}

.circle_show1 {
  border-radius: 50%;
  margin: 6px;
  height: 30px;
  width: 30px;
  background: #409EFF;
  color: white;
  display: flex;
  font-size: 12px;
  font-weight: bold;
  justify-content: center;
  align-items: center;
  box-shadow: 0 0 2px 1px rgba(0, 0, 0, 0.3);
}

.circle_show2 {
  border-radius: 50%;
  margin: 6px;
  height: 30px;
  width: 30px;
  background: white;
  color: #409EFF;
  display: flex;
  font-size: 12px;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  box-shadow: 0 0 2px 1px rgba(0, 0, 0, 0.2);
}

.right-panel1::-webkit-scrollbar {
  width: 0;
}
</style>