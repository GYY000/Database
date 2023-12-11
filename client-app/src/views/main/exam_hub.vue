<template>
  <div class="background_wrap"></div>
  <el-row style="margin-bottom: 20px">
    <el-col :span="4">
      <div style="font-size: 18px;color: dodgerblue;margin-bottom: 5px;font-weight: bold">
        Exam Hub
      </div>
      <div style="font-size: 12px">考试广场</div>
    </el-col>
    <el-col :offset="6" :span="14" style="display: flex;justify-content: right;margin-top: 5px">
      <el-button type="success" @click="dialog_visible = true">
        创建考试
      </el-button>
    </el-col>
  </el-row>

  <el-dialog
      v-model="dialog_visible"
      title="创建考试"
      width="40%"
      draggable
      :before-close="handle_close"
      center>
    <create_exam_form @change_visible="change_dialog_visible" @refresh="refresh"></create_exam_form>
  </el-dialog>
  <el-row style="margin-top: 20px">
    <el-col :span="18">
      <el-card style="width: 100%">
        <el-row style="margin-bottom: 15px;color: grey;font-weight: bold">
          考试汇总
        </el-row>
        <el-col :span="24">
          <el-table
              :data="exams"
              style="width: 100%"
              height="400px"
              stripe
          >
            <el-table-column property="eid" label="id" width="70px" sortable/>
            <el-table-column property="exam_name" label="考试名"/>
            <el-table-column property="start_time" label="考试时间" sortable/>
            <el-table-column property="duration" label="持续时间" sortable/>
            <el-table-column property="creator_name" label="创建者"/>
            <el-table-column label="">
              <template #default="scope">
                <el-button v-if="scope.row.is_inside === 'false'" type="primary"
                           @click="join_exam(scope.row.eid)">加入考试</el-button>
                <el-button v-else type="primary"
                           @click="into_exam(scope.row.eid)">进入考试</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-card>
    </el-col>

    <el-col style="margin-left: 15px" :span="5">
      <el-card style="width: 100%;height: 400px;overflow-y: scroll">
        <el-row style="margin-bottom: 15px;color: grey;font-weight: bold">
          正在进行
        </el-row>
        <el-col :span="24">
          <el-table
              :data="ongoing_exam"
              style="width: 100%"
              stripe
          >
            <el-table-column property="exam_name" label="考试名"/>
            <el-table-column label="">
              <template #default="scope">
                <el-button v-if="scope.row.is_inside === 'false'" type="primary" style="width: 70px"
                           @click="join_exam(scope.row.eid)">加入考试</el-button>
                <el-button v-else type="primary"
                           @click="into_exam(scope.row.eid)">进入考试</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-card>
    </el-col>
  </el-row>
</template>

<script>
import {ref} from "vue";
import {ElMessage, ElMessageBox} from "element-plus";
import ques_group_card from "@/views/main/question_component/ques_group_card.vue";
import {
  fetch_all_coming_test,
  participate_exam,
} from "@/views/main/api";
import userStateStore from "@/store";
import {Search} from "@element-plus/icons-vue";
import Create_exam_form from "@/views/main/exam/create_exam_form.vue";
import router from "@/router";

export default {
  name: "exam_hub",
  computed: {
    Search() {
      return Search
    }
  },
  components: {Create_exam_form, ques_group_card},

  setup() {
    const dialog_visible = ref(false)
    const store = userStateStore()
    const exams = ref([])
    const ongoing_exam = ref([])

    const isWithinTimeRange = (start_time, duration) => {
      const startTime = new Date(start_time);
      const currentTime = new Date();
      const endTime = new Date(startTime.getTime() + duration * 1000);
      return currentTime >= startTime && currentTime <= endTime;
    }

    const init = () => {
      fetch_all_coming_test(store.getUserId).then(
          (res) => {
            exams.value = []
            ongoing_exam.value = []
            for (let i = 0; i < res.eid_list.length; i++) {
              if (isWithinTimeRange(res.start_time_list[i], res.duration_list[i])) {
                ongoing_exam.value.push(
                    {
                      "eid": res.eid_list[i],
                      "start_time": res.start_time_list[i],
                      "duration": formatDuration(res.duration_list[i]),
                      "creator_name": res.creator_name_list[i],
                      "exam_name": res.exam_name_list[i],
                      "is_inside": res.is_inside_list[i],
                    }
                )
              }
              exams.value.push(
                  {
                    "eid": res.eid_list[i],
                    "start_time": res.start_time_list[i],
                    "duration": formatDuration(res.duration_list[i]),
                    "creator_name": res.creator_name_list[i],
                    "exam_name": res.exam_name_list[i],
                    "is_inside": res.is_inside_list[i]
                  }
              )
            }
          }
      )
    }

    const formatDuration = (seconds) => {
      // 计算小时、分钟和剩余秒数
      const hours = Math.floor(seconds / 3600);
      const minutes = Math.floor((seconds % 3600) / 60);

      // 构建格式化字符串
      let durationString = '';
      if (hours > 0) {
        durationString += hours + 'h ';
      }
      if (minutes > 0) {
        durationString += minutes + 'min';
      }
      return durationString.trim(); // 去除字符串两端的空格
    }

    init()

    const join_exam = (eid) => {
      participate_exam(store.getUserId, eid).then(
          (res) => {
            if(res.is_successful === 'true') {
              ElMessage.success("报名成功，请及时参与")
              router.go(0)
            }
          }
      )
    }

    const into_exam = (eid) => {
      router.push('/panel_del_index/do_exam/' + eid)
    }

    const change_dialog_visible = (flag) => {
      dialog_visible.value = flag
    }

    const handle_close = (done) => {
      ElMessageBox.confirm('确定取消创建考试吗')
          .then(() => {
            done();
          })
          .catch(() => {
            // catch error
          });
    };

    const refresh = () => {
      router.go(0);
    }

    return {
      dialog_visible,
      handle_close,
      change_dialog_visible,
      refresh,
      exams,
      join_exam,
      into_exam,
      ongoing_exam
    }
  }
}
</script>

<style scoped>
.groups-container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: left;
  width: 100%;
}

.background_wrap {
  background: #f2f2f2;
  opacity: 80%;
}

.top_panel {
  display: flex;
  flex-direction: row-reverse;
  width: auto;
}

.top_panel span {
  padding-left: 5px;
}
</style>