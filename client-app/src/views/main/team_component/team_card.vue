<template>
  <el-card :body-style="{ padding: '0px' }" shadow="hover"
           style="width:23%; border-radius: 3%;margin-top: 10px;">
    <el-skeleton :loading="flag" animated>
      <template #template>
        <el-skeleton-item variant="image" class="image-container"/>
      </template>
      <template #default>
        <div class="image-container">
          <img :src="avatar_url" alt="can't find the jpg">
        </div>
      </template>
    </el-skeleton>

    <div class="card_layout">
      <div class="set_title">
        {{ group_name }}
      </div>
      <div style="display: flex;width: 100%;justify-content: center">
        <div class="seperator"></div>
      </div>
      <div class="set_content">
        {{ introduction }}
      </div>
      <div class="set_create">
        <div style="padding: 2px">{{ creator_name }} {{ date }}</div>
      </div>
      <div class="footer">
        <el-col :span="9">
          <el-button type="primary" :icon="Edit" @click="to_intro"
                     class="button">
            简介
          </el-button>
        </el-col>
        <el-col :span="9" :offset="2">
          <el-button type='success' v-if="inside" :icon="Menu" class="button" @click="enter_in">
            详情
          </el-button>
          <el-button type="primary" v-else :icon="Plus" class="button" @click="joinReq">
            加入
          </el-button>
        </el-col>
      </div>
    </div>

    <el-dialog v-model="intro_dialog_open" :show-close="false" draggable>
      <template #header="{ close, titleId}">
        <div class="my-header">
          <div :id="titleId" class="edit_title">Team</div>
        </div>
      </template>
      <team_introduction :tid="tid" :team_name="group_name"
                         :date="date" :avatar="avatar_url" :creator="creator_name"
                         :introduction="introduction"/>
    </el-dialog>
  </el-card>
</template>

<script>
import {Edit, MagicStick, Menu, Plus, Remove, TopRight} from "@element-plus/icons-vue";
import {apply_for_team, check_inside_group, fetch_team_avatar} from "@/views/main/api";
import {ref} from "vue";
import userStateStore from "@/store";
import router from "@/router";
import {ElMessage} from "element-plus";
import Team_introduction from "@/views/main/team_component/team_introduction.vue";

export default {
  name: "team_card",
  components: {Team_introduction},
  props: ['creator_name', 'group_name', 'date', 'tid', 'group_name', 'introduction'],

  setup(props, context) {
    const avatar_url = ref(null)
    const flag = ref(true)
    const store = userStateStore()
    const inside = ref(false)
    const intro_dialog_open = ref(false)

    const enter_in = () => {
      router.push('/manage_team/' + props.tid)
    }

    const func = () => {
      fetch_team_avatar(props.group_name).then(
          (data) => {
            avatar_url.value = data.avatar.startsWith('/9j')
                ? 'data:image/jpg;base64,' + data.avatar : 'data:image/png;base64,' + data.avatar;
            flag.value = false;
          });
      check_inside_group(store.getUserId, props.group_name).then(
          (data) => {
            inside.value = data.is_inside === 'true' || props.creator_name === store.getUserName
          }
      );
    }

    const to_intro = () => {
      intro_dialog_open.value = true
    }

    const joinReq = () => {
      apply_for_team(props.creator_name, props.group_name, store.getUserId).then(
          (response) => {
            if (response.have_applied === 'true') {
              ElMessage({
                message: '您已申请过，请等待创建者批准',
                showClose: true,
                type: 'error',
              })
            } else if (response.is_successful === 'true') {
              ElMessage({
                message: '发送成功',
                showClose: true,
                type: 'success',
              })
            } else {
              ElMessage({
                message: '申请失败',
                showClose: true,
                type: 'error',
              })
            }
          }
      )
    }

    func()
    return {
      avatar_url,
      flag,
      store,
      to_intro,
      inside,
      joinReq,
      intro_dialog_open,
      enter_in
    }
  },

  computed: {
    Menu() {
      return Menu
    },
    Remove() {
      return Remove
    },
    Plus() {
      return Plus
    },
    TopRight() {
      return TopRight
    },
    MagicStick() {
      return MagicStick
    },
    Edit() {
      return Edit
    }
  }
}
</script>

<style scoped>
.card_layout {
  display: flex;
  justify-content: center;
  flex-direction: column;
  width: 90%;
  padding-left: 5%;
  /*max-width: 300px;*/
  height: 150px
}

.image-container {
  width: 100%;
  height: 250px;
  overflow: hidden;
}

.image-container img {
  width: 100%;
  height: 250px;
  object-fit: cover;
}

.set_title {
  padding-top: 5px;
  font-weight: bold;
  font-size: 18px;
  color: #1169ea;
  height: 20%;
  display: flex;
  justify-content: center;
}

.set_content {
  padding-top: 10px;
  height: 50%;
  font-size: 10px;
  width: 100%;
  display: flex;
  justify-content: center;
}

.set_create {
  padding-top: 10px;
  padding-left: 5%;
  padding-right: 5%;
  font-size: 10px;
  color: rgb(86, 94, 108);
  height: 15%;
  display: flex;
  justify-content: center;
}

.footer {
  height: 25%;
  padding-left: 5%;
  padding-right: 5%;
  padding-bottom: 3%;
  display: flex;
  justify-content: center;
}

.button {
  margin-top: 8px;
  height: 70%;
  width: 100%;
}

.seperator {
  height: 1px;
  width: 70%;
  position: relative;
  margin-top: 5px;
  background: linear-gradient(to bottom right, rgba(214, 216, 220, 0.96) 0%,
  rgba(70, 64, 255, 0.56) 60%,
  rgba(214, 216, 220, 0.96) 100%);
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.2);
}

@font-face {
  font-family: 'Lobster';
  src: url('/src/assets/fonts/Lobster-1-4-1.otf') format('truetype');
}

.edit_title {
  font-size: 50px;
  font-family: 'Lobster', cursive;
  display: flex;
  justify-content: center;
}
</style>