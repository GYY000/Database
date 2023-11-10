<template>
  <el-card :body-style="{ padding: '0px' }" shadow="hover"
           style="width:23%; border-radius: 3%;margin-top: 10px">
    <div class="card_layout">
      <div class="image-container" v-if="flag === true">
        <img :src="avatar_url" alt="can't find the jpg">
      </div>
      <div class="set_title">
        {{ group_name }}
        <div class="seperator"></div>
      </div>
      <div class="set_content">
        {{ introduction }}
      </div>
      <div class="set_create">
        <div style="padding: 2px">{{ creator_name }} {{ date }}</div>
      </div>
      <div class="footer" v-if="creator_name === store.getUserName">
        <el-button type="primary" :icon="TopRight" class="button"/>
        <el-button type="primary" :icon="MagicStick" class="button"/>
      </div>
      <div v-else class="footer">

      </div>
    </div>
  </el-card>
</template>

<script>
import {Edit, MagicStick, TopRight} from "@element-plus/icons-vue";
import {fetch_team_avatar} from "@/views/main/api";
import {ref} from "vue";
import userStateStore from "@/store";

export default {
  name: "team_card",
  props: ['creator_name', 'group_name', 'date', 'introduction'],

  setup(props){
    const avatar_url = ref(null)
    const flag = ref(false)
    const store = userStateStore()

    const func = () => {
      fetch_team_avatar(props.group_name).then(
          (data) => {
            avatar_url.value = data.avatar.startsWith('/9j')
                ? 'data:image/jpg;base64,' + data.avatar : 'data:image/png;base64,' + data.avatar;
            flag.value = true;
          })
    }
    func()
    return{
      avatar_url,
      flag,
      store
    }
  },

  computed: {
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
  max-width: 300px;
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
  font-weight: bold;
  font-size: 18px;
  color: #1169ea;
  height: 30%;
}

.set_content {
  height: 30%;
  font-size: 10px;
}

.set_create {
  font-size: 10px;
  color: rgb(86, 94, 108);
  height: 15%;
}

.footer {
  height: 25%;
  display: flex;
}

.button {
  margin-top: 8px;
  height: 70%;
  width: 30%;
  padding-right: 5px;
}

.seperator {
  height: 1px;
  width: 90%;
  position: relative;
  margin-top: 5px;
  background: linear-gradient(to bottom right, rgba(214, 216, 220, 0.96) 0%,
  rgba(70, 64, 255, 0.56) 60%,
  rgba(214, 216, 220, 0.96) 100%);
  box-shadow: 0 -2px 4px rgba(0, 0, 0, 0.2);
}
</style>