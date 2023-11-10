<template>
  <el-card :body-style="{ padding: '0px' }" shadow="hover"
           style="width:23%; border-radius: 3%;margin-top: 10px">
    <div class="image-container" v-if="flag === true">
      <img :src="avatar_url" alt="can't find the jpg">
    </div>
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
        <el-button type="primary" :icon="Edit" @click="toEdit" v-if="creator_name === store.getUserName" class="button"
                   round>
          管理用户组
        </el-button>
        <div v-else>
          <el-button type='danger' v-if="inside" :icon="Remove" class="button" @click="exit" round>
            退出
          </el-button>
          <el-button type="primary" v-else :icon="Plus" class="button" @click="joinReq" round>
            加入
          </el-button>
        </div>

      </div>
    </div>
  </el-card>
</template>

<script>
import {Edit, MagicStick, Plus, Remove, TopRight} from "@element-plus/icons-vue";
import {apply_for_team, check_inside_group, fetch_team_avatar} from "@/views/main/api";
import {ref} from "vue";
import userStateStore from "@/store";
import router from "@/router";
import {ElMessage} from "element-plus";

export default {
  name: "team_card",
  props: ['creator_name', 'group_name', 'date', 'introduction'],

  setup(props, context) {
    const avatar_url = ref(null)
    const flag = ref(false)
    const store = userStateStore()
    const inside = ref(false)

    const func = () => {
      fetch_team_avatar(props.group_name).then(
          (data) => {
            avatar_url.value = data.avatar.startsWith('/9j')
                ? 'data:image/jpg;base64,' + data.avatar : 'data:image/png;base64,' + data.avatar;
            flag.value = true;
          });
      check_inside_group(store.getUserId, props.group_name).then(
          (data) => {
            inside.value = data.is_inside === 'true'
          }
      );
    }

    const toEdit = () => {
      context.emit('try_edit', {flag: true, team_name: props.group_name})
    }

    const exit = () => {
      //TODO:
    }

    const joinReq = () => {
      apply_for_team(props.creator_name, props.group_name, store.getUserId).then(
          (response) => {
            if(response.is_successful === 'true') {
              ElMessage({
                message: '发送成功',
                showClose: true,
                type: 'success',
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
      toEdit,
      inside,
      exit,
      joinReq
    }
  },

  computed: {
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
  flex-direction: column;
  width: 90%;
  padding-left: 5%;
  max-width: 300px;
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
  padding-left: 5%;
  padding-right: 5%;
  height: 50%;
  font-size: 10px;
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
  width: 58%;
  padding-right: 5px;
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
</style>