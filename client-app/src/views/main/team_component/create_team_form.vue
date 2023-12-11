<template>
  <el-form style="padding-bottom: 15px">
    <div v-show="image_src !== ''" class="image-container">
      <img :src="image_src" id="show">
    </div>
    <input id="file" type="file"
           accept="image/jpeg,image/png" ref="upload_img"
           @change="show_pic" style="padding-bottom: 15px"/>
    <el-input v-model="group_name" placeholder="请输入用户团队的名字"
              clearable style="padding-bottom: 10px" maxlength="30"></el-input>
    <el-input v-model="introduction" placeholder="请输入团队简介"
              :autosize="{ minRows: 3, maxRows: 5 }"
              type="textarea"
              clearable maxlength="50"></el-input>
  </el-form>
  <el-button @click="closure">Cancel</el-button>
  <el-button type="primary" @click="transmit">
    Confirm
  </el-button>
</template>

<script>
import {ref} from "vue";
import userStateStore from "@/store/index";
import {upload_team} from "@/views/main/api";
import {ElMessage} from "element-plus";
import router from "@/router";

export default {
  name: "create_team_group",
  props: ["dialog_visible"],

  setup(_, context) {
    const store = userStateStore()
    const group_name = ref('')
    const set_name = ref('')
    const upload_img = ref(null)
    const image_src = ref('')
    const introduction = ref('')

    const closure = () => {
      upload_img.value = ''
      group_name.value = ''
      image_src.value = ''
      introduction.value = ''
      context.emit('change_visible', false);
    }

    const add_team = () => {
      if (group_name.value === '') {
        ElMessage.error("请填入团队名")
      } else if (introduction.value === '') {
        ElMessage.error("请填入团队介绍")
      } else if (upload_img.value === '') {
        ElMessage.error("请填入团队头像")
      } else {
        let form = new FormData
        form.append("user_id", store.getUserId)
        form.append("group_name", group_name.value)
        form.append('introduction', introduction.value)
        form.append('file', upload_img.value.files[0])
        upload_team(form).then(
            (res) => {
              if (res.is_successful === "true") {
                ElMessage({
                  message: '上传成功',
                  showClose: true,
                  type: 'success',
                })
                set_name.value = ''
                group_name.value = ''
                router.go(0)
              } else {
                ElMessage({
                  message: '上传失败，请稍后再试',
                  showClose: true,
                  type: 'error',
                })
              }
            }
        )
      }
    }

    const show_pic = (event) => {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        image_src.value = e.target.result;
      };
      reader.readAsDataURL(file);
    }

    const transmit = () => {
      add_team()
      closure()
    }

    return {
      closure,
      group_name,
      transmit,
      add_team,
      upload_img,
      show_pic,
      image_src,
      introduction
    }
  }
}
</script>

<style scoped>
.image-container {
  width: 300px;
  height: 200px;
  overflow: hidden;
  padding-bottom: 10px;
}

.image-container img {
  width: auto;
  height: 100%;
  object-fit: cover;
}
</style>