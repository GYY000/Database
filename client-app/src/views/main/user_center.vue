<template>
  <img src="src/assets/image/inside_backpage1.jpg" class="background">
  <div class="all-container">
    <div class="container">
      <div class="title">U s e r C e n t e r</div>
      <div class="seperator"></div>
      <div class="show_info">
        <div class="left-column">
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
          </el-upload>
        </div>
        <div class="right-column">
          <div class="title_sub">
            <div style="display: flex; align-items: center; justify-content: center;">
              <el-icon style="padding-right: 10px">
                <User/>
              </el-icon>
              {{ store.getUserName }}
            </div>
          </div>
          <div class="seperator_sub"></div>
          <div class="info-box">
            <div class="left-column1" style="flex: 1">
              <div class="row-left">
                <el-tag type="" effect="dark" class="show_tag">
                  <div style="display: flex; align-items: center; justify-content: center;">
                    <el-icon>
                      <Calendar/>
                    </el-icon>
                    <span>注册日期</span>
                  </div>
                </el-tag>
              </div>
              <div class="row-left">
                <el-tag type="" effect="dark" class="show_tag">
                  <div style="display: flex; align-items: center; justify-content: center;">
                    <el-icon>
                      <Notification/>
                    </el-icon>
                    <span>箴言</span>
                  </div>
                </el-tag>
              </div>
            </div>
            <div class="right-column" style="flex: 3">
              <div class="row-right">
                <div style="display: flex; align-items: center; justify-content: center;">
                  <span class="info_font">{{ store.getRegisterDate }}</span>
                </div>
              </div>
              <div class="row-right">
                <div style="display: flex; align-items: center; justify-content: center;">
                  <span class="info_font">还是待做咧</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="footer">
        <div class="button-wrapper">
          <el-button color="#626aef" @click="back_to_main">mainpage</el-button>
          <el-button type="primary" @click="logout">logout</el-button>
        </div>

      </div>

    </div>
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
    //const is_editing_user_name = ref(false)
    //TODO: on server change here
    const action_url = ref("http://127.0.0.1:8000/upload_avatar?user_id=" + store.getUserId)
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

    const back_to_main = () => {
      router.push('/')
    }
    const logout = () => {
      store.logout()
      router.push({path: '/log_reg'});
    };

    return {
      handleBeforeUpload,
      src1,
      action_url,
      handleAvatarSuccess,
      store,
      back_to_main,
      logout
    }
  }
}
</script>

<style scoped>
.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}

.avatar {
  width: 80%;
  height: 80%;
  left: 10%;
  position: relative;
  border-radius: 50%;
}

.container {
  position: relative;
  width: 70%;
  height: 100vh;
  background: linear-gradient(to bottom right, #a8edea 0%, #fed6e3 100%);
  opacity: 90%;
  backdrop-filter: blur(2px);
  border-radius: 10px;
  box-shadow: 0 14px 28px rgba(0, 0, 0, .25), 0 10px 10px rgba(0, 0, 0, .22);
}

.left-column {
  flex: 1;
  display: flex;
  justify-content: flex-end;
}

.left-column1 {
  flex: 1;
}

.avatar-uploader {
  padding-top: 3%;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 40%;
  padding-right: 50px;
}

.right-column {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.row-left {
  height: 30px;
  padding-top: 15px;
  width: 80px;
  flex: 1; /* 将每一行等分为三份 */
}

.row-right {
  height: 30px;
  padding-top: 15px;
  width: 130px;
  flex: 1;
}

.show_tag {
  font-weight: bold;
  width: 100%;
  height: 100%
}

.show_info {
  display: flex;
  height: 40vh;
}

.info_font {
  padding: 5px;
  font-weight: bold;
  color: #4a5260;
  font-family: "Microsoft YaHei";
}

.info-box {
  display: flex;
}

.title {
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Lobster', cursive;
  color: #1169ea;
  font-size: 50px;
  font-weight: 600;
  padding-top: 10px;
}

.seperator {
  height: 1px;
  width: 80%;
  position: relative;
  left: 10%;
  background: linear-gradient(to bottom right, rgba(70, 64, 255, 0.56) 0%, rgba(254, 214, 227, 0.87) 100%);
  margin: 10px 0;
  box-shadow: 0px -2px 4px rgba(0, 0, 0, 0.2);
}

.title_sub {
  display: flex;
  justify-content: left;
  align-items: center;
  font-family: "Microsoft YaHei";
  color: #4a5260;
  font-size: 30px;
  font-weight: 600;
  padding-top: 10px;
}

.seperator_sub {
  height: 1px;
  width: 80%;
  position: relative;
  background: linear-gradient(to bottom right, rgba(70, 64, 255, 0.56) 0%, rgba(254, 214, 227, 0.87) 100%);
  margin: 10px 0;
}

.background {
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  position: fixed;
  z-index: -1;
}

.footer {
  width: 100%;
  display: flex;
  justify-content: center;
}

.button-wrapper {
  width: 30%;
  display: flex;
  justify-content: space-around;
}

.all-container {
  display: flex;
  justify-content: center;
}
</style>