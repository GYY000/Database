<template>
  <img src="@/assets/image/background3.jpg" class="background">
  <div class="secbackground"></div>
  <div class="center_class">
    <div class="main_container">
      <el-row style="margin-top: 30px">
        <el-col :span="6" :offset="15">
          <el-button :icon="Upload" @click="open_form" class="control_button"
                     style="margin-right: 8px">
            添加题目
          </el-button>
          <el-button type="danger" icon="Close" @click="del_set" class="control_button"
                     style="margin-right: 8px">
            删除题集
          </el-button>
        </el-col>
      </el-row>
      <div class="title center_class">
        <span>
          <el-skeleton :loading="photo_flag" animated>
            <template #template>
              <el-skeleton-item variant="image" class="image_container1"/>
            </template>
            <template #default>
              <img :src="profile_photo" class="image_container1" alt="can't find the jpg">
            </template>
          </el-skeleton>
        </span>
        <span style="height: 45px;margin-left: 10px">
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
      </div >
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
          <ques_display :ques="ques"></ques_display>
        </div>
      </div>
    </div>
  </div>

  <el-dialog
      v-model="edit_show"
      :show-close="true"
      center>
    <template #header="{ close, titleId}">
      <div class="edit-header">
        <div :id="titleId" class="edit_title">上传问题</div>
      </div>
    </template>
    <upload_ques_form :qs_id="ques_set_id" @close="close_form"/>
  </el-dialog>
</template>

<script>
import userStateStore from "@/store";
import {ref} from "vue";
import Ques_display from "@/views/quesDoing/ques_display.vue";
import {del_ques_set, fetch_ques_info} from "@/views/main/api";
import Upload_ques_form from "@/views/quesDoing/upload_ques_form.vue";
import Update_ques_form from "@/views/quesDoing/update_ques_form.vue";
import {DocumentChecked, Edit, Plus, Upload} from "@element-plus/icons-vue";
import router from "@/router";
import {useRouter} from "vue-router";
import {ElMessage} from "element-plus";

export default {
  name: 'edit_ques_group',
  computed: {
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
  components: {Upload_ques_form, Ques_display, Update_ques_form},
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
    const edit_show = ref(false)
    const edit_mode = ref(false)
    const profile_photo = ref('')
    const photo_flag = ref(true)
    const sum_score = ref(0.0)
    const ques_set_name = ref('')
    const introduction = ref()
    const ques_set_id = ref()

    const handlePageChange = (val) => {
      page.value = val;
      display_ques.value = questions.value.slice(page.value * page_size.value + 1, page_size.value)
    }

    const init = () => {
      let router = useRouter()
      ques_set_id.value = router.currentRoute.value.params.qs_id
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
            for (let i = 0; i < questions.value.length; i = i + 1) {
              sum_score.value = sum_score.value + questions.value[i].score
            }
            for (let ques of Object.values(questions.value)) {
              if (ques.content.type === '选择') {
                statistic.value[0].choice = statistic.value[0].choice + 1
                statistic.value[1].choice = statistic.value[1].choice + ques.score
              } else if (ques.content.type === '填空') {
                statistic.value[0].blank = statistic.value[0].blank + 1
                statistic.value[1].blank = statistic.value[1].blank + ques.score
              } else if (ques.content.type === '问答') {
                statistic.value[0].quesAndAns = statistic.value[0].quesAndAns + 1
                statistic.value[1].quesAndAns = statistic.value[1].quesAndAns + ques.score
              } else if (ques.content.type === '复合') {
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

    const close_form = () => {
      edit_show.value = false
    }

    const open_form = () => {
      edit_show.value = true
    }

    init()

    const open_edit = () => {
      edit_mode.value = true
    }

    const close_edit = () => {
      edit_mode.value = false
    }

    const del_set = () => {
      del_ques_set(ques_set_name.value).then(
          (res) => {
            if(res.is_successful === 'true') {
              ElMessage.success("删除成功")
              router.push('/question_hub')
            } else {
              ElMessage.error("删除失败，请重新再试")
            }
          }
      )
    }

    const change_info = (data) => {
      sum_score.value = 0
      questions.value[data.id].score = data.score
      for (let i = 0; i < questions.value.length; i = i + 1) {
        sum_score.value = sum_score.value + questions.value[i].score
      }
    }

    return {
      store,
      questions,
      handleCurrentChange: handlePageChange,
      display_ques,
      show,
      currentPage,
      edit_show,
      open_form,
      close_form,
      page_size,
      edit_mode,
      open_edit,
      close_edit,
      profile_photo,
      photo_flag,
      change_info,
      sum_score,
      introduction,
      ques_set_name,
      statistic,
      del_set,
      ques_set_id
    }
  }
}
</script>

<style scoped>
.secbackground {
  top: 8%;
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
  top: 3%;
  left: 5%;
  width: 90%;
  height: 100vh;
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

.edit_title {
  font-family: "Microsoft YaHei";
  font-weight: bold;
  font-size: 30px;
}

.center_class {
  display: flex;
  justify-content: center;
  align-items: center;
}

.control_button {
  width: 8%;
  min-width: 90px;
}

.image_container1 {
  width: 45px;
  height: 45px;
  object-fit: cover;
  border-radius: 50%;
}

.intro_font {
  font-size: 15px;
  color: grey;
}

.intro {
  color: grey;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: normal;
  min-height: calc(3em * 1.2);
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