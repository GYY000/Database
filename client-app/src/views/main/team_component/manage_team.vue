<template>
  <img src="@/assets/image/background3.jpg" class="background">
  <div class="center_class">
    <div class="main_container">
      <el-row style="margin-bottom: 20px">
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
      <el-row>
        <el-col :span="18">
          <el-row>
            <el-col :span="7">
              <el-card>
                <el-row>
                  <el-col :span="10">
                    <div style="width: 50px;height: 50px;
                    background: dodgerblue;border-radius: 20%">
                      <img src="@/assets/image/申请.png"
                           style="width: 40px;height: 40px;margin-top: 5px;margin-left: 5px"/>
                    </div>
                  </el-col>
                  <el-col :span="13">
                    <div style="font-size: 18px;font-weight: bold;margin-bottom: 3px">
                      近七天申请
                    </div>
                    <div>
                      {{ history_applications }}
                    </div>
                  </el-col>
                </el-row>
              </el-card>
            </el-col>
            <el-col :span="7" :offset="1">
              <el-card>
                <el-row>
                  <el-col :span="10">
                    <div style="width: 50px;height: 50px;
                    background: dodgerblue;border-radius: 20%">
                      <img src="@/assets/image/好友.png"
                           style="width: 40px;height: 40px;margin-top: 5px;margin-left: 5px"/>
                    </div>
                  </el-col>
                  <el-col :span="13">
                    <div style="font-size: 18px;font-weight: bold;margin-bottom: 3px">
                      团队成员数
                    </div>
                    <div>
                      {{ user_list.length }}
                    </div>
                  </el-col>
                </el-row>
              </el-card>
            </el-col>
            <el-col :span="7" :offset="1">
              <el-card>
                <el-row>
                  <el-col :span="10">
                    <div style="width: 50px;height: 50px;
                    background: dodgerblue;border-radius: 20%">
                      <img src="@/assets/image/问卷.png"
                           style="width: 40px;height: 40px;margin-top: 5px;margin-left: 5px"/>
                    </div>
                  </el-col>
                  <el-col :span="13">
                    <div style="font-size: 18px;font-weight: bold;margin-bottom: 3px">
                      问题组数
                    </div>
                    <div>
                      {{ ques_set_list.length }}
                    </div>
                  </el-col>
                </el-row>
              </el-card>
            </el-col>
          </el-row>
          <el-row>
            <el-table :data="history_display" style="width: 96%;margin-top: 20px;height: 420px">
              <el-table-column label="团队动态">
                <template #default="scope">
                  <history_entry :info="scope.row"></history_entry>
                </template>
              </el-table-column>
            </el-table>
          </el-row>
        </el-col>
        <el-col :span="6">
          <el-card>
            <div style="display: flex;
            justify-content: center;margin-bottom: 10px;
            font-family: Lobster; font-size: 28px">
              Team Profile
            </div>
            <img :src="avatar" style="height: 300px;width: 100%;object-fit: cover;border-radius: 6%"/>
            <div style="margin-left: 5px;margin-right: 5px;
              margin-top: 10px;font-weight: bold">
              团队介绍
            </div>
            <div style="margin-left: 5px;margin-right: 5px;margin-top: 10px;font-size: 13px;height: 100px">
              {{ introduction }}
            </div>
          </el-card>
        </el-col>
      </el-row>
      <el-row style="margin-top: 20px">
        <el-col :span="12">
          <el-row style="margin-bottom: 10px;">
            <el-button type="primary" :icon="ChatSquare">
              群发消息
            </el-button>
            <el-button type="danger" :icon="Close">
              删除成员
            </el-button>
            <el-button type="primary" :icon="EditPen">
              发起考试
            </el-button>
          </el-row>
          <el-row>
            <el-table
                ref="multipleTableRef"
                :data="user_list"
                style="width: 100%"
                height="90%"
                stripe
                @selection-change="handleSelectionChange"
            >
              <el-table-column type="selection"/>
              <el-table-column property="id" label="id" sortable/>
              <el-table-column property="name" label="用户名" sortable/>
              <el-table-column property="date" label="加入时间" sortable/>
            </el-table>
          </el-row>
        </el-col>
        <el-col :span="11" :offset="1">
          <el-table>

          </el-table>
        </el-col>
      </el-row>
      <div style="height: 150px"/>
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
  <el-dialog v-model="group_message_dialog">

  </el-dialog>
</template>

<script>
import {ref} from "vue";
import {useRouter} from "vue-router";
import {
  del_members,
  del_team,
  fetch_all_member,
  fetch_all_team_ques_set, fetch_history_application, fetch_history_team,
  fetch_team_info,
  update_team,
} from "@/views/main/api";
import Judge_ans_view from "@/views/quesDoing/judge_ans_view.vue";
import Ques_do_display from "@/views/quesDoing/ques_do_display.vue";
import userStateStore from "@/store";
import {ElMessage} from "element-plus";
import History_entry from "@/views/main/team_component/history_entry.vue";
import {ChatSquare, Close, EditPen} from "@element-plus/icons-vue";

function compareFn(a, b) {
  if (a.date > b.date) {
    return -1;
  }
  if (a.date < b.date) {
    return 1;
  }
  return 0;
}

export default {
  name: "manage_team",
  computed: {
    EditPen() {
      return EditPen
    },
    Close() {
      return Close
    },
    ChatSquare() {
      return ChatSquare
    }
  },
  components: {History_entry, Ques_do_display, Judge_ans_view},

  setup() {
    const history_display = ref([])
    const history_applications = ref(0)
    const ques_set_list = ref([])
    const user_list = ref([])
    const creator_name = ref()
    const team_name = ref()
    const introduction = ref()
    const avatar = ref()
    const date = ref()
    const store = userStateStore()
    const exit_confirm_dialog = ref(false)
    const edit_dialog = ref(false)
    const group_message_dialog = ref(false)
    const change_avatar = ref('')
    const hand_in_avatar = ref('')
    const edit_introduction = ref('')
    const multipleTableRef = ref(null);
    const multipleSelection = ref([]);

    const handleSelectionChange = (val) => {
      multipleSelection.value = val;
      console.log(multipleSelection.value)
    }

    const init = () => {
      let router = useRouter()
      fetch_all_member(router.currentRoute.value.params.tid).then(
          (res) => {
            for (let i = 0; i < res.uid_list.length; i++) {
              user_list.value.push({
                id: res.uid_list[i],
                name: res.name_list[i],
                date: res.register_date_list[i]
              })
              history_display.value.push({
                name: res.name_list[i],
                date: res.register_date_list[i],
                type: 'enter'
              })
            }
            fetch_history_team(router.currentRoute.value.params.tid).then(
                (res) => {
                  for (let i = 0; i < res.user_name_list.length; i++) {
                    history_display.value.push(
                        {
                          name: res.user_name_list[i],
                          date: res.date_list[i],
                          type: 'do_prob',
                          ques_set_name: res.ques_set_list[i]
                        }
                    )
                  }
                  fetch_all_team_ques_set(router.currentRoute.value.params.tid).then(
                      (res) => {
                        for (let i = 0; i < res.qsid_list.length; i++) {
                          ques_set_list.value.push(
                              {
                                name: res.name_list[i],
                                id: res.qsid_list[i],
                                creator: res.creator_list[i],
                                date: res.date_list[i]
                              }
                          )
                          history_display.value.push(
                              {
                                ques_set_name: res.name_list[i],
                                name: res.creator_list[i],
                                date: res.date_list[i],
                                type: "new_set"
                              }
                          )
                        }
                        history_display.value.sort(compareFn)
                        history_display.value.slice(0, 10)
                      }
                  )

                }
            )
          }
      )
      fetch_history_application(router.currentRoute.value.params.tid).then(
          (res) => {
            history_applications.value = res.application_sum
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
      ques_set_list,
      user_list,
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
      cancel_edit,
      history_display,
      history_applications,
      group_message_dialog,
      handleSelectionChange,
      multipleTableRef,
      multipleSelection
    }
  }
}
</script>

<style scoped>

@font-face {
  font-family: 'Lobster';
  src: url('/src/assets/fonts/Lobster-1-4-1.otf') format('truetype');
}

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