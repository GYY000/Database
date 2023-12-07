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
        <el-card style="width: 100%;">
          <el-row v-if="creator_name === store.getUserName" style="margin-bottom: 15px;color: grey;font-weight: bold">
            成员管理
          </el-row>
          <el-row v-else style="margin-bottom: 15px;color: grey;font-weight: bold">
            成员信息
          </el-row>
          <el-col :span="24">
            <el-row v-if="creator_name === store.getUserName" style="margin-bottom: 10px;">
              <el-button type="primary" :icon="ChatSquare" @click="open_group_message">
                群发消息
              </el-button>
              <el-button type="primary" :icon="EditPen">
                发起考试
              </el-button>
              <el-button type="danger" :icon="Close" @click="open_del_member">
                删除成员
              </el-button>
            </el-row>
            <el-row>
              <el-table
                  ref="multipleTableRef"
                  :data="user_list"
                  style="width: 100%"
                  height="400px"
                  stripe
                  @selection-change="handleSelectionChange"
              >
                <el-table-column v-if="creator_name === store.getUserName" type="selection"/>
                <el-table-column property="id" label="id" sortable/>
                <el-table-column property="name" label="用户名" sortable/>
                <el-table-column property="date" label="加入时间" sortable/>
                <el-table-column property="do_prob_sum" label="做题数" sortable/>
                <el-table-column property="accuracy" label="正确率" sortable/>
                <el-table-column label="">
                  <template #default="scope">
                    <el-button type="primary" @click="member_show(scope.row)">查看详情</el-button>
                  </template>
                </el-table-column>
              </el-table>
            </el-row>
          </el-col>
        </el-card>
      </el-row>
      <el-row style="margin-top: 20px">
        <el-card style="width: 100%;">
          <el-row v-if="creator_name === store.getUserName" style="margin-bottom: 15px;color: grey;font-weight: bold">
            问题组管理
          </el-row>
          <el-row v-else style="margin-bottom: 15px;color: grey;font-weight: bold">
            问题组汇总
          </el-row>
          <el-col :span="24">
            <el-table
                :data="ques_set_list"
                style="width: 100%"
                height="400px"
                stripe
            >
              <el-table-column property="id" label="id" width="70px" sortable/>
              <el-table-column property="name" label="问题组名" sortable/>
              <el-table-column property="date" label="创建时间" sortable/>
              <el-table-column property="creator" label="创建者" sortable/>
              <el-table-column property="ques_sum" label="题目数" width="90px" sortable/>
              <el-table-column property="do_time" label="完成次数" width="110px" sortable/>
              <el-table-column property="average_score" label="平均分" sortable/>
              <el-table-column label="">
                <template #default="scope">
                  <el-button type="primary" @click="ques_set_show(scope.row)">查看详情</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-col>
        </el-card>
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
  <el-dialog v-if="creator_name === store.getUserName" v-model="group_message_dialog">
    <template #header>
      <div style="display: flex;justify-content: center">
        <el-icon style="color: dodgerblue;height: 25px;width: 25px;margin-right: 5px">
          <ChatSquare/>
        </el-icon>
        <span style="font-size: 18px;color:dodgerblue">群发消息</span>
      </div>
    </template>
    <el-row>
      <el-col :offset="1" :span="22" style="font-size: 15px;color:grey;margin-bottom: 10px">
        消息内容
      </el-col>
    </el-row>
    <el-row>
      <el-col :offset="1" :span="22">
        <el-input type="textarea" v-model="message_content"
                  :autosize="{ minRows: 3}" placeholder="请输入消息内容"
                  style=""/>
      </el-col>
    </el-row>
    <el-row style="margin-top: 15px" align="center">
      <el-col :offset="1" :span="2" style="font-size: 15px;margin-top: 3px;color: grey">接收人</el-col>
      <el-col :offset="1" :span="10">
        <el-select
            v-model="option_user"
            placeholder="Please select"
            style="width: 240px"
            multiple
            disabled
        />
      </el-col>
    </el-row>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="send_message">
          发送
        </el-button>
        <el-button type="danger" @click="exit_message_send">
          取消
        </el-button>
      </span>
    </template>
  </el-dialog>
  <el-dialog v-if="creator_name === store.getUserName" v-model="del_member_dialog">
    <template #header>
      <div style="display: flex;justify-content: center">
        <el-icon style="color:indianred;height: 25px;width: 25px;margin-right: 5px">
          <CloseBold/>
        </el-icon>
        <span style="font-size: 18px;color:indianred;font-weight: bold">删除成员</span>
      </div>
    </template>
    <el-row style="margin-top: 15px" align="center">
      <el-col :offset="1" :span="3" style="font-size: 15px;margin-top: 3px;color: grey">
        所选成员
      </el-col>
      <el-col :offset="1" :span="13">
        <el-select
            v-model="option_user"
            placeholder="Please select"
            style="width: 240px"
            multiple
            disabled
        />
      </el-col>
    </el-row>
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="confirm_del_members">
          确定
        </el-button>
        <el-button type="danger" @click="cancel_del_members">
          取消
        </el-button>
      </span>
    </template>
  </el-dialog>
  <el-dialog v-model="member_info_dialog" style="width:400px" draggable>
    <template #header>
      <div style="display: flex;justify-content: center">
        <span style="font-size: 35px;color:dodgerblue;font-family: Lobster;font-weight: bold">Member</span>
      </div>
    </template>
    <div style="display: flex;justify-content: center">
      <div>
        <el-skeleton :loading="member_avatar_flag" animated>
          <template #template>
            <el-skeleton-item variant="image" style="width: 100px; height: 100px; border-radius: 50%"/>
          </template>
          <template #default>
            <img :src="member_info.avatar" style="width: 100px; height: 100px;border-radius: 50%">
          </template>
        </el-skeleton>
      </div>
      <div style="display: flex; flex-direction: column;padding-left: 20px">
        <div style="font-size:17px; padding-bottom: 5px;display: flex;justify-content: left">
          <span style="font-weight: bold;color: #409EFF">{{ member_info.name }}</span>
        </div>
        <div style="padding-bottom: 5px;">
          加入于 {{ member_info.date }}
        </div>
        <div style="padding-bottom: 5px;">
          共完成 {{ member_info.do_prob_sum }} 道题目
        </div>
        <div style="padding-bottom: 5px;">
          正确率 {{ member_info.accuracy }}
        </div>
      </div>
    </div>
  </el-dialog>
  <el-dialog v-model="ques_set_info_dialog" style="width: 500px">
    <template #header>
      <div style="display: flex;justify-content: center">
        <span style="font-size: 35px;color:dodgerblue;font-weight: bold;font-family: Lobster">QuesSet</span>
      </div>
    </template>
    <el-row>
      <el-col :span="11" :offset="1">
        <el-skeleton :loading="ques_set_avatar_flag" animated>
          <template #template>
            <el-skeleton-item variant="image" style="width: 100%; height: 180px"/>
          </template>
          <template #default>
            <img :src="ques_set_info.avatar"
                 style="width: 100%; height: 180px;object-fit: cover">
          </template>
        </el-skeleton>
      </el-col>
      <el-col :span="11" style="margin-left: 10px">
        <div style="margin-bottom: 8px;font-weight: bold;
        color: dodgerblue;margin-right: 10px;margin-left: 5px;font-size: 20px">
          {{ques_set_info.name}}
        </div>
        <div style="margin-bottom: 8px;color:grey;
        margin-right: 10px;margin-left: 5px">
          {{ques_set_info.date}}
        </div>
        <div style="margin-bottom: 8px;color:grey;
        margin-right: 10px;margin-left: 5px">
          由{{ques_set_info.creator}}创建
        </div>
        <div style="margin-bottom: 8px;color:grey;
        margin-right: 10px;margin-left: 5px">
          <el-tag style="width: 70px">完成次数</el-tag>&nbsp{{ques_set_info.do_time}}
        </div>
        <div style="margin-bottom: 8px;color:grey;
        margin-right: 10px;margin-left: 5px">
          <el-tag style="width: 70px">平均分</el-tag>&nbsp{{ques_set_info.average_score}}
        </div>
        <div>
          <el-button v-if="creator_name === store.getUserName" type="primary" style="margin-left: 3px" @click="goto_ques_set(ques_set_info.id)">
            详情
          </el-button>
          <el-button v-else type="primary" style="margin-left: 3px" @click="goto_ques_set(ques_set_info.id)">
            做题
          </el-button>
        </div>
      </el-col>
    </el-row>
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
  fetch_avatar,
  fetch_history_application,
  fetch_history_team,
  fetch_set_avatar,
  fetch_team_info,
  send_team_message,
  update_team,
} from "@/views/main/api";
import Judge_ans_view from "@/views/quesDoing/judge_ans_view.vue";
import Ques_do_display from "@/views/quesDoing/ques_do_display.vue";
import userStateStore from "@/store";
import {ElMessage} from "element-plus";
import History_entry from "@/views/main/team_component/history_entry.vue";
import {ChatSquare, Close, CloseBold, EditPen} from "@element-plus/icons-vue";
import User_show_card from "@/views/main/team_component/user_show_card.vue";
import router from "@/router";

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
  components: {User_show_card, CloseBold, History_entry, Ques_do_display, Judge_ans_view},

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
    const user_selection = ref([]);
    const message_content = ref('')
    const option_user = ref([])
    const del_member_dialog = ref(false)
    const member_info_dialog = ref(false)
    const member_info = ref(null)
    const member_avatar_flag = ref(true)
    const ques_set_info_dialog = ref(false)
    const ques_set_avatar_flag = ref(true)
    const ques_set_info = ref(null)

    const goto_ques_set = (id) => {
      if(creator_name.value === store.getUserName) {
        router.push('/edit_ques_group/' + id)
      } else {
        router.push('panel_del_index/do_prob/' + id)
      }
    }

    const handleSelectionChange = (val) => {
      user_selection.value = val;
      option_user.value = []
      for (let i = 0; i < val.length; i++) {
        option_user.value.push(val[i].name)
      }
    }

    const ques_set_show = (info) => {
      ques_set_info.value = {
        avatar: '',
        name: info.name,
        id: info.id,
        date: info.date,
        creator: info.creator,
        ques_sum: info.ques_sum,
        do_time: info.do_time,
        average_score: info.average_score,
      }
      ques_set_avatar_flag.value = true
      ques_set_info_dialog.value = true
      fetch_set_avatar(info.name).then(
          (res) => {
            ques_set_info.value = {
              avatar: res.avatar.startsWith('/9j')
                ? 'data:image/jpg;base64,' + res.avatar : 'data:image/png;base64,' + res.avatar,
              name: info.name,
              id: info.id,
              date: info.date,
              creator: info.creator,
              ques_sum: info.ques_sum,
              do_time: info.do_time,
              average_score: info.average_score,
            }
            ques_set_avatar_flag.value = false
          }
      )
    }

    const member_show = (info) => {
      member_info.value = {
        avatar: '',
        name: info.name,
        date: info.date,
        accuracy: info.accuracy,
        do_prob_sum: info.do_prob_sum
      }
      member_avatar_flag.value = true
      member_info_dialog.value = true
      fetch_avatar(info.name).then(
          (res) => {
            member_info.value = {
              avatar: res.profile_photo.startsWith('/9j')
                  ? 'data:image/jpg;base64,' + res.profile_photo : 'data:image/png;base64,' + res.profile_photo,
              name: info.name,
              date: info.date,
              accuracy: info.accuracy,
              do_prob_sum: info.do_prob_sum
            }
            member_avatar_flag.value = false
          }
      )
    }

    const init = () => {
      let router1 = useRouter()
      fetch_all_member(router1.currentRoute.value.params.tid).then(
          (res) => {
            console.log(res)
            for (let i = 0; i < res.uid_list.length; i++) {
              user_list.value.push(
                  {
                    id: res.uid_list[i],
                    name: res.name_list[i],
                    date: res.register_date_list[i],
                    do_prob_sum: res.do_prob_sum_list[i],
                    accuracy: (res.accuracy_list[i] * 100).toFixed(1) + '%'
                  }
              )
              history_display.value.push({
                name: res.name_list[i],
                date: res.register_date_list[i],
                type: 'enter'
              })
            }
            fetch_history_team(router1.currentRoute.value.params.tid).then(
                (res) => {
                  for (let i = 0; i < res.user_name_list.length; i++) {
                    history_display.value.push(
                        {
                          name: res.user_name_list[i],
                          date: res.date_list[i],
                          type: 'do_prob',
                          ques_set_name: res.ques_set_list[i],
                        }
                    )
                  }
                  fetch_all_team_ques_set(router1.currentRoute.value.params.tid).then(
                      (res) => {
                        for (let i = 0; i < res.qsid_list.length; i++) {
                          ques_set_list.value.push(
                              {
                                name: res.name_list[i],
                                id: res.qsid_list[i],
                                creator: res.creator_list[i],
                                date: res.date_list[i],
                                ques_sum: res.ques_sum_list[i],
                                do_time: res.do_time_list[i],
                                average_score: res.average_score_list[i].toFixed(1)
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
      fetch_history_application(router1.currentRoute.value.params.tid).then(
          (res) => {
            history_applications.value = res.application_sum
          }
      )
      fetch_team_info(router1.currentRoute.value.params.tid).then(
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
      let router1 = useRouter()
      let form = new FormData
      form.append("tid", router1.currentRoute.value.params.tid)
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

    const send_message = () => {
      let uids = []
      let router1 = useRouter()
      for (let user of user_selection.value) {
        uids.push(user.id)
      }
      send_team_message(uids, router1.currentRoute.value.params.tid,
          message_content.value).then(
          (res) => {
            if (res.is_successful === 'true') {
              ElMessage.success("发送成功")
            } else {
              ElMessage.error("发送失败")
            }
          }
      )
    }

    const exit_message_send = () => {
      group_message_dialog.value = false
      message_content.value = ''
    }

    const exit = () => {
      let router1 = useRouter()
      if (creator_name.value === store.getUserName) {
        del_team(router1.currentRoute.value.params.tid).then(
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

    const open_group_message = () => {
      if (user_selection.value.length === 0) {
        ElMessage.error("请先选择消息发送给的用户")
      } else {
        group_message_dialog.value = true
      }
    }

    const open_del_member = () => {
      if (user_selection.value.length === 0) {
        ElMessage.error("请先选择要删除的成员")
      } else {
        del_member_dialog.value = true
      }
    }

    const confirm_del_members = () => {
      let select_uids = []
      for (let user in user_selection.value) {
        select_uids.push(user.id)
      }
      let router1 = useRouter()
      del_members(select_uids, router1.currentRoute.value.params.tid).then(
          (res) => {
            if (res.is_successful === 'true') {
              ElMessage.success('删除成功')
            } else {
              ElMessage.error("删除失败")
            }
            del_member_dialog.value = false
          }
      )
    }

    const cancel_del_members = () => {
      del_member_dialog.value = false
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
      user_selection,
      open_group_message,
      send_message,
      message_content,
      exit_message_send,
      option_user,
      open_del_member,
      del_member_dialog,
      confirm_del_members,
      cancel_del_members,
      member_info_dialog,
      member_info,
      member_show,
      member_avatar_flag,
      ques_set_show,
      ques_set_info_dialog,
      ques_set_avatar_flag,
      ques_set_info,
      goto_ques_set
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
  left: 2%;
  width: 96%;
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