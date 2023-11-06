<template>
  <div class="container">
    <img :src="src1" class="avatar">
    <el-upload
        class="avatar-uploader"
        :action=action_url
        :before-upload="handleBeforeUpload"
        :auto-upload="true"
        :show-file-list="false"
        accept=".jpg,.png"
        :on-success="handleAvatarSuccess"
    >
      <img v-if="src1" :src="src1" class="avatar">
      <div>点击即可更换头像</div>
    </el-upload>
  </div>
</template>

<script>
import {ref} from "vue";
import userStateStore from "@/store/index";
import {ElMessage} from "element-plus";
import {fetch_user_info} from "@/views/loginInterface/loginAPI";
import {UploadFilled} from '@element-plus/icons-vue'
import router from "@/router";

export default {
  name: "user_center",
  components: {UploadFilled},
  setup() {
    const store = userStateStore()
    const src1 = ref(store.getProfilePhoto)
    //TODO: on server change here
    const action_url = ref("http://127.0.0.1:8000/upload_avatar?user_name=" + store.getUserName)
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
      fetch_user_info(store.getUserName).then((res) => {
        store.login_store_info(res);
        router.go(0)
      });
      src1.value = store.getProfilePhoto
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
}

.container {
  overflow: hidden;
  width: 100%;
  height: 100vh;
  max-width: 100%;
  backdrop-filter: blur(2px);
  background: #f2f2f2;
  opacity: 95%;
}
</style>