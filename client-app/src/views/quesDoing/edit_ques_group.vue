<template>
  <img src="src/assets/image/background3.jpg" class="background">
  <div class="secbackground"></div>
  <div class="center_class">
    <div class="main_container">
    <div class="title center_class">
      {{ store.getQuesGroupName }}
    </div>
    <div class="center_class">
      <el-button :icon="Upload" @click="open_form" class="control_button">添加题目</el-button>
      <el-button :icon="DocumentChecked" type="primary" @click="close_edit" v-if="edit_mode" class="control_button">保存</el-button>
      <el-button :icon="Edit" type="primary" @click="open_edit" v-else class="control_button">编辑</el-button>
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
      <ques_display v-for="ques in display_ques" :ques="ques" :edit_mode="edit_mode"></ques_display>
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
  components: {Upload_ques_form, Ques_display},
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

    const handleCurrentChange = (val) => {
      page.value = val;
      display_ques.value = questions.value.slice(page.value * page_size.value + 1, page_size.value)
    }

    const init = () => {
      fetch_ques_info(store.ques_group_name).then(
          (res) => {
            questions.value = res.questions
            show.value = true
            display_ques.value = questions.value.slice((page.value - 1) * page_size.value,
                (page.value - 1) * page_size.value + page_size.value)
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

    return {
      store,
      questions,
      handleCurrentChange,
      display_ques,
      show,
      currentPage,
      edit_show,
      open_form,
      close_form,
      page_size,
      edit_mode,
      open_edit,
      close_edit
    }
  }
}
</script>

<style scoped>
.secbackground {
  top: 3%;
  left: 2%;
  width: 96%;
  height: 100vh;
  position: fixed;
  z-index: -1;
  opacity: 70%;
  background-color: #f2f2f2;
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
  font-family: 'YouSheBiaoTiHei', sans-serif;
  font-size: 50px;
  color: blue;
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
  width:8%;
  min-width: 90px;
  margin-right: 10px;
}
</style>