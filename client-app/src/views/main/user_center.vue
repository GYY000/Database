<template>
  <el-row style="height: 200px">
    <el-col :span="11" style="display: flex;justify-content: right;margin-right: 15px">
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
    </el-col>
    <el-col :span="11">
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
        </div>
        <div class="right-column" style="flex: 3">
          <div class="row-right">
            <div style="display: flex; align-items: center; justify-content: center;">
              <span class="info_font">{{ store.getRegisterDate }}</span>
            </div>
          </div>
        </div>

      </div>
      <el-button type="primary" @click="open_change_password"
                 style="margin-top: 15px">更改密码
      </el-button>
      <el-button type="danger" @click="logout" style="margin-top: 15px">退出登录</el-button>
    </el-col>
  </el-row>
  <el-dialog v-model="password_dialog" style="width:400px" draggable>
    <template #header>
      <div style="display: flex;justify-content: center">
        <span style="font-size: 35px;color:dodgerblue;font-family: Lobster;font-weight: bold">修改密码</span>
      </div>
    </template>
    <el-form
        label-position="left"
        label-width="75px"
        style="max-width: 300px;margin:auto">
      <el-form-item label="密码">
        <el-input v-model="old_password" :show-password="true"/>
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="new_password" :show-password="true"/>
      </el-form-item>
      <el-form-item label="确认密码">
        <el-input v-model="confirm_password" :show-password="true"/>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="confirm_change">
          确定
        </el-button>
        <el-button type="danger" @click="cancel_change">
          取消
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import {ref} from "vue";
import userStateStore from "@/store/index";
import {ElMessage} from "element-plus";
import {fetch_user_info} from "@/views/loginInterface/loginAPI";
import {UploadFilled} from '@element-plus/icons-vue'
import router from "@/router";
import {change_password} from "@/views/main/api";

export default {
  name: "user_center",
  components: {UploadFilled},
  setup() {
    const store = userStateStore()
    const src1 = ref(store.getProfilePhoto)
    const password_dialog = ref(false)
    const old_password = ref('')
    const new_password = ref('')
    const confirm_password = ref('')

    const confirm_change = () => {
      if (new_password.value === confirm_password.value) {
        change_password(store.getUserId, old_password.value, new_password.value).then(
            (res) => {
              if (res.old_password_fault === 'true') {
                ElMessage.error("原有密码输入错误")
              } else if (res.is_successful === 'true') {
                ElMessage.success("修改成功")
                password_dialog.value = false
              } else {
                ElMessage.error("修改失败，请稍后再试")
              }
            }
        )
      } else {
        ElMessage.error("请确认新密码是否一致")
      }
    }

    const cancel_change = () => {
      password_dialog.value = false
    }

    const open_change_password = () => {
      password_dialog.value = true
    }

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
      logout,
      open_change_password,
      password_dialog,
      old_password,
      new_password,
      confirm_password,
      confirm_change,
      cancel_change
    }
  }
}
</script>

<style scoped>
.avatar-uploader .el-upload:hover {
  border: 1px dashed #409EFF;
}

.avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
}

.left-column1 {
  flex: 1;
}

.avatar-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 150px;
  height: 150px;
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

.info_font {
  padding: 5px;
  font-weight: bold;
  color: #4a5260;
  font-family: "Microsoft YaHei";
}

.info-box {
  display: flex;
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

.background {
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  position: fixed;
  opacity: 10%;
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
</style>