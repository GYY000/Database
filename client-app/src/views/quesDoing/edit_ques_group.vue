<template>
  <img src="src/assets/image/background3.jpg" class="background">
  <div class="secbackground"></div>
  <div class="center_class">
    <div class="main_container">
      <div class="title center_class">
        {{ store.getQuesGroupName }}
      </div>
      <el-row style="margin-top: 15px">
        <el-col :span="4" :offset="8" style="margin-right: 10px">
          <el-skeleton :loading="photo_flag" animated>
            <template #template>
              <el-skeleton-item variant="image" style="width: 140px;height: 140px;border-radius: 50%"/>
            </template>
            <template #default>
              <img :src="profile_photo" class="image_container1" alt="can't find the jpg">
            </template>
          </el-skeleton>
        </el-col>
        <el-col :span="5">
          <div class="intro_font" style="margin-bottom: 5px">总题数 {{ questions.length }}</div>
          <div class="intro_font" style="margin-bottom: 5px">总分数 {{ sum_score }}</div>
          <div class="intro" style="margin-bottom: 5px"> {{ introduction }}</div>
          <div>
            <el-button :icon="Upload" @click="open_form" class="control_button"
                       style="margin-right: 8px">添加题目
            </el-button>
            <el-button :icon="DocumentChecked" type="primary" @click="close_edit" v-if="edit_mode"
                       class="control_button">
              保存
            </el-button>
            <el-button :icon="Edit" type="primary" @click="open_edit" v-else class="control_button">
              编辑
            </el-button>
          </div>
          <!-- TODO: Tags-->
        </el-col>
      </el-row>
      <div class="center_class">

      </div>
      <div v-if="show">
        <el-pagination
            v-model:current-page="currentPage"
            :page-size="page_size"
            :hide-on-single-page="true"
            layout="prev, pager, next, jumper"
            :total="questions.length"
            @current-change="handleCurrentChange"
        />
        <ques_display v-for="ques in display_ques" :ques="ques"></ques_display>
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
    <upload_ques_form @close="close_form"/>
  </el-dialog>
</template>

<script>
import userStateStore from "@/store";
import {ref} from "vue";
import Ques_display from "@/views/quesDoing/ques_display.vue";
import {fetch_ques_info} from "@/views/main/api";
import Upload_ques_form from "@/views/quesDoing/upload_ques_form.vue";
import Update_ques_form from "@/views/quesDoing/update_ques_form.vue";
import {DocumentChecked, Edit, Plus, Upload} from "@element-plus/icons-vue";

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
    const introduction = ref()

    const handlePageChange = (val) => {
      page.value = val;
      display_ques.value = questions.value.slice(page.value * page_size.value + 1, page_size.value)
    }

    const init = () => {
      fetch_ques_info(store.ques_group_name).then(
          (res) => {
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
      introduction
    }
  }
}
</script>

<style scoped>
.secbackground {
  top: 10%;
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
  font-size: 45px;
  font-weight: bold;
  color: black;
}

.edit_title {
  font-family: "Microsoft YaHei";
  font-weight: bold;
  font-size: 30px;
}

.center_class {
  display: flex;
  justify-content: center;
}

.control_button {
  width: 8%;
  min-width: 90px;
}

.image_container1 {
  width: 140px;
  height: 140px;
  object-fit: cover;
  border-radius: 50%;
}

.intro_font {
  font-size: 15px;
  color: grey;
}

.intro{
  color: grey;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: normal;
  min-height: calc(3em * 1.2);
}
</style>