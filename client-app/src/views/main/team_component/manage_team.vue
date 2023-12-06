<template>
  <img src="@/assets/image/background3.jpg" class="background">
  <div class="center_class">
    <div class="main_container">
      <el-row>
        <el-col :span="4" v-if="creator_name === store.getUserName">
          <div style="font-size: 18px;color: dodgerblue;margin-bottom: 5px;font-weight: bold">
            {{ team_name }}
          </div>
          <div style="font-size: 12px">管理团队</div>
        </el-col>
        <el-col :span="4" v-else>
          <div style="font-size: 18px;color: dodgerblue;margin-bottom: 5px">
            {{ team_name }}
          </div>
          <div style="font-size: 12px">查看动态</div>
        </el-col>
        <el-col :offset="15" :span="4">
          <el-button type="danger" v-if="creator_name === store.getUserName" @click="open_exit">
            注销
          </el-button>
          <el-button type="danger" @click="open_exit" v-else>
            退出
          </el-button>
          <el-button v-if="creator_name === store.getUserName" @click="open_edit">
            编辑
          </el-button>
        </el-col>
      </el-row>
    </div>
  </div>
  <el-dialog
      v-model="exit_confirm_dialog"
      width="30%"
  >
    <span v-if="creator_name === store.getUserName">您确定注销团队吗</span>
    <span v-else>您确定退出团队吗</span>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="danger" @click="exit">
          确定
        </el-button>
      </span>
    </template>
  </el-dialog>
  <el-dialog
      v-if="creator_name === store.getUserName"
      v-model="edit_dialog"
      title="编辑信息"
      width="30%">
    <el-form>
      <el-upload
          class="avatar-uploader"
          action="#"
          :show-file-list="false"
          :auto-upload="false"
          :on-change="handle_avatar"
      >
        <img v-if="change_avatar" :src="change_avatar" class="avatar"/>
        <el-icon v-else class="avatar-uploader-icon">
          <Plus/>
        </el-icon>
      </el-upload>
      <div class="form-label">团队名</div>
      <el-input v-model="team_name" placeholder="请输入团队名"
                clearable style="padding-bottom: 10px" maxlength="15" disabled></el-input>
      <div class="form-label">问题组介绍</div>
      <el-input v-model="edit_introduction" placeholder="请输入团队简介"
                :autosize="{ minRows: 3, maxRows: 5 }"
                type="textarea"
                clearable maxlength="30"></el-input>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="hand_in_edit">
          提交
        </el-button>
        <el-button type="danger" @click="cancel_edit">
          取消
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script>
import {ref} from "vue";
import {useRouter} from "vue-router";
import {
  del_members,
  del_team,
  fetch_all_member,
  fetch_all_team_ques_set,
  fetch_team_info, hand_in_ans, update_team,
  upload_ques_set
} from "@/views/main/api";
import Judge_ans_view from "@/views/quesDoing/judge_ans_view.vue";
import Ques_do_display from "@/views/quesDoing/ques_do_display.vue";
import userStateStore from "@/store";
import {ElMessage} from "element-plus";

export default {
  name: "manage_team",
  components: {Ques_do_display, Judge_ans_view},

  setup() {
    const qs_name_list = ref([])
    const qs_id_list = ref([])
    const qs_creator_list = ref([])
    const qs_date_list = ref([])
    const u_id_list = ref([])
    const u_name_list = ref([])
    const u_register_date_list = ref([])
    const creator_name = ref()
    const team_name = ref()
    const introduction = ref()
    const avatar = ref()
    const date = ref()
    const store = userStateStore()
    const exit_confirm_dialog = ref(false)
    const edit_dialog = ref(false)
    const change_avatar = ref('')
    const hand_in_avatar = ref('')
    const edit_introduction = ref('')

    const init = () => {
      let router = useRouter()
      fetch_all_member(router.currentRoute.value.params.tid).then(
          (res) => {
            u_id_list.value = res.uid_list
            u_name_list.value = res.name_list
            u_register_date_list.value = res.register_date_list
          }
      )
      fetch_all_team_ques_set(router.currentRoute.value.params.tid).then(
          (res) => {
            qs_name_list.value = ref(res.name_list)
            qs_id_list.value = ref(res.qsid_list)
            qs_creator_list.value = ref(res.creator_list)
            qs_date_list.value = ref(res.date_list)
          }
      )
      fetch_team_info(router.currentRoute.value.params.tid).then(
          (res) => {
            creator_name.value = res.creator_name
            team_name.value = res.team_name
            introduction.value = res.introduction
            avatar.value = res.avatar.startsWith('/9j')
                ? 'data:image/jpg;base64,' + res.avatar : 'data:image/png;base64,' + res.avatar;
            change_avatar.value = res.avatar.startsWith('/9j')
                ? 'data:image/jpg;base64,' + res.avatar : 'data:image/png;base64,' + res.avatar;
            date.value = res.date
          }
      )
    }

    const handle_avatar = (uploadFile, uploadFiles) => {
      if (uploadFile.raw.type !== "image/jpeg" && uploadFile.raw.type !== "image/png") {
        ElMessage.error('Avatar picture must be JPG format!');
        return false;
      }
      const reader = new FileReader();
      reader.onload = (e) => {
        change_avatar.value = e.target.result;
      };
      reader.readAsDataURL(uploadFile.raw);
      hand_in_avatar.value = uploadFile.raw;
      return true;
    }

    const open_edit = () => {
      edit_dialog.value = true
    }

    const hand_in_edit = () => {
      let router = useRouter()
      let form = new FormData
      form.append("tid", router.currentRoute.value.params.tid)
      form.append('introduction', introduction.value)
      form.append('file', hand_in_avatar.value)
      form.append('change_avatar', hand_in_avatar.value !== '')
      update_team(form).then(
          (res) => {
            if (res.is_successful === "true") {
              ElMessage({
                message: '修改成功',
                showClose: true,
                type: 'success',
              })
            } else {
              ElMessage({
                message: '修改失败，请稍后再试',
                showClose: true,
                type: 'error',
              })
            }
            edit_dialog.value = false
          }
      )
    }

    const cancel_edit = () => {
      edit_introduction.value = introduction.value
      hand_in_avatar.value = ''
      change_avatar.value = avatar.value
      edit_dialog.value = false
    }

    const open_exit = () => {
      exit_confirm_dialog.value = true
    }

    const exit = () => {
      let router = useRouter()
      if (creator_name.value === store.getUserName) {
        del_team(router.currentRoute.value.params.tid).then(
            (res) => {
              if (res.is_successful === 'true') {
                ElMessage({
                  message: '注销成功',
                  showClose: true,
                  type: 'success',
                })
              } else {
                ElMessage({
                  message: '注销失败',
                  showClose: true,
                  type: 'error',
                })
              }
            }
        )
      } else {
        let array = []
        array.push(store.getUserId)
        del_members(array).then(
            (res) => {
              if (res.is_successful === 'true') {
                ElMessage({
                  message: '成功退出',
                  showClose: true,
                  type: 'success',
                })
              } else {
                ElMessage({
                  message: '退出失败',
                  showClose: true,
                  type: 'error',
                })
              }
            }
        )
      }
    }

    init()

    return {
      qs_name_list,
      qs_creator_list,
      qs_date_list,
      qs_id_list,
      u_id_list,
      u_name_list,
      u_register_date_list,
      avatar,
      change_avatar,
      introduction,
      creator_name,
      date,
      team_name,
      store,
      edit_dialog,
      exit_confirm_dialog,
      edit_introduction,
      open_edit,
      open_exit,
      exit,
      handle_avatar,
      hand_in_edit,
      cancel_edit
    }
  }
}
</script>

<style scoped>
.background {
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  position: fixed;
  z-index: -1;
  opacity: 3%;
}

.main_container {
  left: 5%;
  width: 90%;
}

.center_class {
  display: flex;
  justify-content: center;
  align-items: center;
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
</style>