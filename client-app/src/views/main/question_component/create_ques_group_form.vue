<template>
  <el-form>
    <el-upload
        class="avatar-uploader"
        action="#"
        :show-file-list="false"
        :auto-upload="false"
        :on-change="handle_change"
    >
      <img v-if="image_src" :src="image_src" class="avatar"/>
      <el-icon v-else class="avatar-uploader-icon">
        <Plus/>
      </el-icon>
    </el-upload>
    <div class="form-label">问题组名称</div>
    <el-input v-model="set_name" placeholder="请输入问题组的名字"
              clearable style="padding-bottom: 10px" maxlength="30"></el-input>
    <div class="form-label">问题组介绍</div>
    <el-input v-model="introduction" placeholder="请输入问题组的简介"
              :autosize="{ minRows: 3, maxRows: 5 }"
              type="textarea"
              clearable maxlength="50"></el-input>
    <div class="form-label" style="margin-bottom: 0px">问题组类型</div>
    <div>
      <el-radio-group v-model="is_public" class="ml-4">
        <el-radio label="public" size="large">公有</el-radio>
        <el-radio label="group" size="large">组间共享</el-radio>
      </el-radio-group>
      <el-input v-if="is_public !== 'public'" placeholder="请输入组名" v-model="group_name" clearable
                style="padding-bottom: 15px"></el-input>
    </div>
  </el-form>
  <el-button @click="closure">Cancel</el-button>
  <el-button type="primary" @click="transmit">
    Confirm
  </el-button>
</template>

<script>
import {ref} from "vue";
import userStateStore from "@/store/index";
import {check_inside_group, upload_ques_set} from "@/views/main/api";
import {ElMessage} from "element-plus";
import {Plus} from "@element-plus/icons-vue";
import router from "@/router";

export default {
  name: "create_ques_group",
  props: ["dialog_visible"],
  emits: ['refresh', 'change_visible'],

  setup(_, context) {
    const store = userStateStore()
    const is_public = ref('public')
    const group_name = ref('')
    const set_name = ref('')
    const avatar = ref('')
    const image_src = ref('')
    const introduction = ref('')
    const upload_img = ref(null)

    const closure = () => {
      avatar.value = ''
      set_name.value = ''
      group_name.value = ''
      image_src.value = ''
      introduction.value = ''
      context.emit('change_visible', false)
    }

    const handle_change = (uploadFile, uploadFiles) => {
      if (uploadFile.raw.type !== "image/jpeg" && uploadFile.raw.type !== "image/png") {
        ElMessage.error('Avatar picture must be JPG format!');
        return false;
      }
      const reader = new FileReader();
      reader.onload = (e) => {
        image_src.value = e.target.result;
      };
      reader.readAsDataURL(uploadFile.raw);
      avatar.value = uploadFile.raw;
      return true;
    }

    const add_ques_set = () => {
      let form = new FormData
      form.append("user_id", store.getUserId)
      if (is_public.value === 'group') {
        form.append("group_name", group_name.value)
      } else {
        form.append("group_name", 'none')
      }
      form.append('introduction', introduction.value)
      form.append('set_name', set_name.value)
      form.append('file', avatar.value)
      //TODO: 后续可加入tag
      upload_ques_set(form).then(
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

    const show_pic = (event) => {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        image_src.value = e.target.result;
      };
      reader.readAsDataURL(file);
    }

    const transmit = () => {
      if (is_public.value === 'public') {
        add_ques_set()
        closure()
      } else {
        const boolean = ref(false)
        check_inside_group(store.getUserId, group_name.value).then(
            (res) => {
              boolean.value = res.is_inside === "true"
            }
        ).then(
            () => {
              if (boolean.value) {
                add_ques_set()
                closure()
              } else {
                ElMessage({
                  message: '您不在用户组内，请重新确认',
                  showClose: true,
                  type: 'error',
                })
              }
            }
        )
      }
    }

    return {
      closure,
      is_public,
      group_name,
      transmit,
      set_name,
      add_ques_set,
      avatar,
      show_pic,
      image_src,
      introduction,
      handle_change,
      upload_img
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

.avatar-uploader .avatar {
  width: 178px;
  height: 178px;
  display: block;
  object-fit: cover;
}
</style>

<style>
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
  margin-bottom: 15px;
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}

.form-label {
  font-size: 15px;
  font-weight: bold;
  margin-bottom: 8px;
}
</style>