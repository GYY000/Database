<template>
  <img src="src/assets/image/background2.jpg" class="background">
  <div class="secbackground"></div>
  <div class="main_container">
    <div class="title">
      {{ store.getQuesGroupName }}
      做题网站
    </div>
    <el-button @click="open_form"></el-button>
    <div v-if="show">
      <el-pagination
          v-model:current-page="currentPage"
          :page-size="10"
          :hide-on-single-page="true"
          layout="prev, pager, next, jumper"
          :total="ques.length"
          @current-change="handleCurrentChange"
      />
      <div v-for="ques in display_ques">
        <ques_display :ques="ques" @upload_ans="caught_ans"></ques_display>
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

export default {
  name: 'edit_ques_group',
  components: {Upload_ques_form, Ques_display},
  setup() {
    const store = userStateStore()
    const ques = ref([])
    const page = ref(1)
    const display_ques = ref([])
    const show = ref(false)
    const currentPage = ref(1)
    const edit_show = ref(false)

    const handleCurrentChange = (val) => {
      page.value = val;
    }

    const caught_ans = (ans_form) => {

    }

    const init = () => {
      fetch_ques_info(store.ques_group_name).then(
          (res) => {
            ques.value = res
            show.value = false
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

    return {
      store,
      ques,
      handleCurrentChange,
      display_ques,
      caught_ans,
      show,
      currentPage,
      edit_show,
      open_form,
      close_form
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
  z-index: 0;
  opacity: 90%;
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
}

.edit_title {
  font-family: "Microsoft YaHei";
  font-weight: bold;
  font-size: 30px;
}
</style>