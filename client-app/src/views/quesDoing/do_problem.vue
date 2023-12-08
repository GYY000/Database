<template>
  <img src="@/assets/image/background3.jpg" class="background">
  <div class="lower_panel" id="lower_panel">
    <el-row style="width: 100%" class="vertical-align-center">
      <el-col :span="3" style="height: 100%; margin-left: 30px;display: flex;align-items: center"
              @click="open_exit" class="hover_class">
        <el-icon style="width: 40px; height: 45px;margin-top: 12px">
          <ArrowLeft/>
        </el-icon>
        <div style="font-size: 16px;margin-top: 12px;display: inline-block">退出答题</div>
      </el-col>
      <el-col :span="8" :offset="7" style="height: 100%;font-size: 16px;color: #545455">
        {{ ques_set_name }}
      </el-col>
      <el-col :span="5">
        <el-button type="success" style="min-width: 80px;margin-right: 10px" plain round
                   @click="open_hand_in">
          提交
        </el-button>
        <el-button text :icon="Timer" @click="stopTimer">
          <span style="font-size: 16px">{{ formattedTime }}</span>
        </el-button>
      </el-col>
    </el-row>
  </div>
  <div class="secbackground"></div>
  <!-- TODO BackGround -->
  <div class="center_class" v-if="judge_mode === false">
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
          题型情况
        </el-col>
        <el-col :offset="6" :span="12">
          <el-table :data="statistic" style="width: 100%">
            <el-table-column prop="sum" label="汇总"/>
            <el-table-column v-if="statistic[0].choice > 0" prop="choice" label="选择"/>
            <el-table-column v-if="statistic[0].blank > 0" prop="blank" label="填空"/>
            <el-table-column v-if="statistic[0].quesAndAns > 0" prop="quesAndAns" label="问答"/>
            <el-table-column v-if="statistic[0].mixture > 0" prop="mixture" label="复合"/>
          </el-table>
        </el-col>
      </div>
      <div v-if="show" style="margin-top: 15px">
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
          <ques_do_display :ques="ques" :id="(currentPage - 1)* page_size + index"
                           @update_ans="update_ans"></ques_do_display>
        </div>
      </div>
    </div>
  </div>
  <div class="center_class" v-if="judge_mode === true">
    <judge_ans_view :hit_scores="hit_scores" :introduction="introduction"
                    :ans="hand_in_form.answers" :ques_set_name="ques_set_name"
                    :questions="questions"/>
  </div>
  <el-dialog
      v-model="exit_dialog"
      title="退出答题"
      width="30%"
  >
    <span>确定退出吗，退出后您的答题结果不会被保留</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="danger" @click="exit">
          确定
        </el-button>
      </span>
    </template>
  </el-dialog>
  <el-dialog
      v-model="stop_dialog"
      title="准备好继续了吗"
      width="30%"
  >
    <img src="@/assets/image/ready.png" style="width: 350px;height: auto;">
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="regoTimer">
          继续
        </el-button>
      </span>
    </template>
  </el-dialog>
  <el-dialog
      v-model="hand_in_dialog"
      title="上交答案"
      width="30%"
  >
    <div>
      <span v-if="empty_ques === 0">您已全部完成，确定上传答案吗，上传答案之后将不能更改</span>
      <span v-else>您还有{{ empty_ques }}道题目没有完成，确定上传答案吗，上传答案之后将不能更改</span>
    </div>
    <div style="display: flex;justify-content: center;margin-top: 20px">
      <img src="@/assets/image/优秀.png" style="width: 200px;height: 200px;" v-if="empty_ques === 0"/>
      <img src="@/assets/image/再考虑一下.png" style="width: 200px;height: 200px;" v-else/>
    </div>

    <template #footer>
      <span class="dialog-footer">
        <el-button type="danger" @click="hand_in">
          确定
        </el-button>
      </span>
    </template>
  </el-dialog>

  <div class="right-panel1" v-if="panel_switch">
    <div style="display: flex;justify-content: right;margin-right: 10px">
      <el-button size="small" :icon="Minus" @click="switch_panel" round/>
    </div>
    <div style="display: flex; flex-wrap: wrap;margin-left: 10px;margin-right: 10px;margin-top: 10px">
      <div v-for="(item,index) in filled_ques" :class="item === false ? 'circle_show2' : 'circle_show1'">
        {{ index + 1 }}
      </div>
    </div>
  </div>
  <div class="right-panel2" v-else>
    <el-button size="small" :icon="Plus"
               style="display:flex;justify-content: right;margin-right: 10px"
               @click="switch_panel" round>
    </el-button>
  </div>
</template>

<script>
import userStateStore from "@/store";
import {onBeforeUnmount, ref} from "vue";
import Ques_display from "@/views/quesDoing/ques_display.vue";
import {fetch_ques_info, hand_in_ans, string2Array} from "@/views/main/api";
import {ArrowLeft, DocumentChecked, Edit, Minus, Plus, Timer, Upload} from "@element-plus/icons-vue";
import {useRouter} from "vue-router";
import router from "@/router";
import Ques_do_display from "@/views/quesDoing/ques_do_display.vue";
import Judge_ans_view from "@/views/quesDoing/judge_ans_view.vue";

export default {
  name: 'do_problem',
  data() {
    return {
      seconds: 0,
      timerInterval: null,
      stop_dialog: false
    };
  },
  methods: {
    stopTimer() {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
      this.stop_dialog = true;
    },
    regoTimer() {
      this.stop_dialog = false
      this.timerInterval = setInterval(() => {
        this.updateTimer();
      }, 1000);
    },
    startTimer() {
      this.timerInterval = setInterval(() => {
        this.updateTimer();
      }, 1000);
    },
    updateTimer() {
      this.seconds++;
    },
    pad(number) {
      return number < 10 ? '0' + number : number;
    }
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
    this.startTimer();
  },
  beforeDestroy() {
    clearInterval(this.timerInterval);
  },
  computed: {
    Minus() {
      return Minus
    },
    Timer() {
      return Timer
    },
    formattedTime() {
      const hours = Math.floor(this.seconds / 3600);
      const minutes = Math.floor((this.seconds % 3600) / 60);
      const remainingSeconds = this.seconds % 60;
      return `${this.pad(hours)}:${this.pad(minutes)}:${this.pad(remainingSeconds)}`;
    },
    Upload() {
      return Upload
    },
    DocumentChecked() {
      return DocumentChecked
    },
    Edit() {
      return Edit
    },
    Plus() {
      return Plus
    }
  },
  components: {
    Judge_ans_view,
    ArrowLeft, Ques_do_display, Ques_display
  },
  setup() {
    const statistic = ref([
      {
        sum: 0,
        choice: 0,
        blank: 0,
        quesAndAns: 0,
        mixture: 0,
      },
      {
        sum: 0.0,
        choice: 0.0,
        blank: 0.0,
        quesAndAns: 0.0,
        mixture: 0.0,
      },
    ])
    const store = userStateStore()
    const questions = ref([])
    const page = ref(1)
    const display_ques = ref([])
    const show = ref(false)
    const currentPage = ref(1)
    const page_size = ref(10)
    const profile_photo = ref('')
    const photo_flag = ref(true)
    const sum_score = ref(0.0)
    const ques_set_name = ref('')
    const introduction = ref()
    const exit_dialog = ref(false)
    const hand_in_dialog = ref(false)
    const judge_mode = ref(false)
    const hit_scores = ref([])
    const filled_ques = ref([])
    const empty_ques = ref(0)
    const panel_switch = ref(true)

    const hand_in_form = ref(
        {
          qids: [],
          types: [],
          all_scores: [],
          answers: [],
          standard_ans: []
        }
    )

    const handlePageChange = (val) => {
      page.value = val;
      display_ques.value = questions.value.slice(page.value * page_size.value + 1, page_size.value)
    }

    const init = () => {
      let router = useRouter()
      fetch_ques_info(router.currentRoute.value.params.qs_id).then(
          (res) => {
            ques_set_name.value = res.ques_set_name
            questions.value = res.questions
            introduction.value = res.introduction
            show.value = true
            profile_photo.value = res.profile_photo.startsWith('/9j')
                ? 'data:image/jpg;base64,' + res.profile_photo
                : 'data:image/png;base64,' + res.profile_photo;
            photo_flag.value = false
            display_ques.value = questions.value.slice((page.value - 1) * page_size.value,
                (page.value - 1) * page_size.value + page_size.value)
            empty_ques.value = questions.value.length
            for (let i = 0; i < questions.value.length; i = i + 1) {
              sum_score.value = sum_score.value + questions.value[i].score
            }
            for (let ques of Object.values(questions.value)) {
              filled_ques.value.push(false)
              hand_in_form.value.qids.push(ques.id)
              if (ques.content.type === '选择') {
                hand_in_form.value.types.push('选择')
                hand_in_form.value.standard_ans.push(ques.content.ans)
                hand_in_form.value.answers.push('')
                hand_in_form.value.all_scores.push(ques.score)
                statistic.value[0].choice = statistic.value[0].choice + 1
                statistic.value[1].choice = statistic.value[1].choice + ques.score
              } else if (ques.content.type === '填空') {
                hand_in_form.value.types.push('填空')
                hand_in_form.value.standard_ans.push(string2Array(ques.content.ans))
                hand_in_form.value.answers.push(new Array(
                    (string2Array(ques.content.ans)).length).fill(''))
                hand_in_form.value.all_scores.push(ques.score)
                statistic.value[0].blank = statistic.value[0].blank + 1
                statistic.value[1].blank = statistic.value[1].blank + ques.score
              } else if (ques.content.type === '问答') {
                hand_in_form.value.types.push('问答')
                hand_in_form.value.standard_ans.push(ques.content.ans)
                hand_in_form.value.answers.push('')
                hand_in_form.value.all_scores.push(ques.score)
                statistic.value[0].quesAndAns = statistic.value[0].quesAndAns + 1
                statistic.value[1].quesAndAns = statistic.value[1].quesAndAns + ques.score
              } else if (ques.content.type === '复合') {
                let temp_type = []
                let temp_score = []
                let temp_answers = []
                let temp_standard_ans = []
                for (let sub_ques of ques.content.sub_problem) {
                  temp_type.push(sub_ques.type)
                  temp_score.push(sub_ques.score)
                  if (sub_ques.type === '选择' || sub_ques.type === '问答') {
                    temp_standard_ans.push(sub_ques.ans)
                    temp_answers.push('')
                  } else if (sub_ques.type === '填空') {
                    temp_standard_ans.push(string2Array(sub_ques.ans))
                    temp_answers.push(new Array(
                        (string2Array(sub_ques.ans)).length).fill('')
                    )
                  }
                }
                hand_in_form.value.types.push(temp_type)
                hand_in_form.value.standard_ans.push(temp_standard_ans)
                hand_in_form.value.answers.push(temp_answers)
                hand_in_form.value.all_scores.push(temp_score)
                statistic.value[0].mixture = statistic.value[0].mixture + 1
                statistic.value[1].mixture = statistic.value[1].mixture + ques.score
              }
            }
            statistic.value[0].sum = statistic.value[0].choice + statistic.value[0].blank +
                statistic.value[0].quesAndAns + statistic.value[0].mixture
            statistic.value[1].sum = statistic.value[1].choice + statistic.value[1].blank +
                statistic.value[1].quesAndAns + statistic.value[1].mixture
          }
      )
    }

    const update_ans = (data) => {
      hand_in_form.value.answers[data.id] = data.ans
      hand_in_dialog.value = false
      if (filled_ques.value[data.id] === true && data.filled === false) {
        empty_ques.value++
      } else if (filled_ques.value[data.id] === false && data.filled === true) {
        empty_ques.value--
      }
      filled_ques.value[data.id] = data.filled
    }

    init()

    const switch_panel = () => {
      panel_switch.value = !panel_switch.value
    }

    const open_exit = () => {
      exit_dialog.value = true
    }

    const exit = () => {
      router.push('/question_hub')
    }

    const open_hand_in = () => {
      hand_in_dialog.value = true
    }

    const hand_in = () => {
      hand_in_ans(hand_in_form.value).then(
          (res) => {
            hit_scores.value = res.hit_scores
            judge_mode.value = true
            hand_in_dialog.value = false
          }
      )
    }

    return {
      store,
      hand_in_form,
      questions,
      handleCurrentChange: handlePageChange,
      display_ques,
      show,
      currentPage,
      page_size,
      profile_photo,
      photo_flag,
      sum_score,
      introduction,
      ques_set_name,
      statistic,
      hand_in_dialog,
      exit_dialog,
      open_exit,
      open_hand_in,
      exit,
      update_ans,
      hand_in,
      judge_mode,
      hit_scores,
      switch_panel,
      panel_switch,
      filled_ques,
      empty_ques
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