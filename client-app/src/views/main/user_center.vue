<template>
  <div>
    here is user_center
  </div>
  <el-upload
      class="avatar-uploader"
      :action=action_url
      :before-upload="handleBeforeUpload"
      :auto-upload="true"
      :show-file-list="false"
      accept=".jpg,.png"
      :on-success="handleAvatarSuccess"
  >
    <el-icon class="el-icon--upload">
      <upload-filled/>
    </el-icon>
    <img v-if="src1" :src="src1" class="avatar">
    <div class="el-upload__text">
      Drop file here or <em>click to upload</em>
    </div>
  </el-upload>
  <img :src="src1" class="avatar">
</template>

<script>
import {ref} from "vue";
import store from "@/store";
import {ElMessage} from "element-plus";
import {fetch_user_info} from "@/views/loginInterface/loginAPI";
import {UploadFilled} from '@element-plus/icons-vue'
import router from "@/router";

export default {
  name: "user_center",
  components: {UploadFilled},
  setup() {
    const src1 = ref(store.getters.getProfilePhoto)
    const action_url = ref("http://127.0.0.1:8000/upload_img?user_name=" + store.getters.getUserName)
    const handleBeforeUpload = (rawFile) => {
      if (rawFile.type !== 'image/jpeg' && rawFile.type !== "image/png") {
        ElMessage.error('Avatar picture must be JPG/PNG format!')
        return false
      } else if (rawFile.size / 1024 / 1024 > 2) {
        ElMessage.error('Avatar picture size can not exceed 2MB!')
        return false
      }
      return true
    }
    const handleAvatarSuccess = (response, uploadFile) => {
          fetch_user_info(store.getters.getUserName).then((res) => {
            store.dispatch("login_store_info", {accountInfo: res});
            router.push({path: "/user_center"});
          });
          src1.value = store.getters.getProfilePhoto
        }
    return {
      handleBeforeUpload,
      src1,
      action_url,
      handleAvatarSuccess
    }
  }
}
</script>

<style scoped>
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>