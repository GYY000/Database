<template>
  <el-card shadow="hover" style="width:32%; border-radius: 3%;margin-top: 10px">
    <div class="card_layout">
      <div class="l_column">
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
      </div>
      <div class="r_column">
        <div class="set_title">
          {{ set_name }}
          <div class="seperator"></div>
        </div>
        <div class="set_content">
          {{ introduction }}
        </div>
        <div class="set_create">
          <div style="padding: 2px">{{ creator_name }} {{ date }}</div>
        </div>
        <div class="footer">
          <el-button type="primary" :icon="TopRight" class="button" @click="do_problem"/>
          <el-button type="danger" :icon="Edit" class="button"
                     v-if="creator_name === user_name" @click="do_edit"/>
          <div style="flex-grow: 1;"/>
          <svg width="20" height="20" class="star" viewBox="0 0 20 20" style="margin-top: 8px;" @click="clickCollection">
            <path d="M10 14.2L5 17l1-5.6-4-4 5.5-.7 2.5-5 2.5 5 5.6.8-4 4 .9 5.5z"
                  :stroke="isFavorite ? 'gold' : 'black'"
                  :fill="isFavorite ? 'gold' : 'none'"
                  fill-rule="inherit"
                  troke-linejoin="round">
            </path>
          </svg>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script>
import {Edit, MagicStick, TopRight} from "@element-plus/icons-vue";
import {fetch_set_avatar} from "@/views/main/api";
import {ref} from "vue";
import userStateStore from "@/store";
import router from "@/router";
import axios from "axios";

export default {
  name: "ques_group_card",
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
  },

  props: ['creator_name', 'set_name', 'date', 'introduction', "qs_id"],

  setup(props) {
    const avatar_url = ref(null)
    const flag = ref(true)
    const store = userStateStore()
    const user_name = ref(store.user_name)

    const do_problem = () => {
      router.push('panel_del_index/do_prob/' + props.qs_id)
    }

    const do_edit = () => {
      router.push('/edit_ques_group/' + props.qs_id)
    }

    const init = () => {
      fetch_set_avatar(props.set_name).then(
          (data) => {
            avatar_url.value = data.avatar.startsWith('/9j')
                ? 'data:image/jpg;base64,' + data.avatar : 'data:image/png;base64,' + data.avatar;
            flag.value = false;
          })
      axios.post("/in_collection", {uid: store.getUserId, qsid: props.qs_id})
          .then(response => {
            console.log(response.data.value)
            if (response.data.value == 'true') {
              isFavorite.value = true;
            } else {
              isFavorite.value = false;
            } // 在异步操作完成后设置isFavorite的值
          })
          .catch(error => {
            console.error(error);
          });
    }

    init()

    const isFavorite = ref(false);

    const clickCollection = () => {
      if (isFavorite.value) {
        axios.post("/remove_collection", {uid: store.getUserId, qsid: props.qs_id})
            .then(response => {
              isFavorite.value = false;
            })
            .catch(error => {
              console.error(error);
            });
      } else {
        axios.post("/add_collection", {uid: store.getUserId, qsid: props.qs_id})
            .then(response => {
              isFavorite.value = true;
            })
            .catch(error => {
              console.error(error);
            });
      }
    }
    return {
      avatar_url,
      flag,
      store,
      user_name,
      do_problem,
      do_edit,
      isFavorite,
      clickCollection
    }
  },

}
</script>

<style scoped>
.card_layout {
  display: flex;
  max-width: 400px;
}

.l_column {
  flex-grow: 2;
  max-width: 300px;
}

.r_column {
  flex-grow: 3;
}

.image-container {
  width: 150px; /* 指定容器的宽度 */
  height: 130px; /* 指定容器的高度 */
  overflow: hidden; /* 裁剪超出容器的部分 */
}

.image-container img {
  width: 130px;
  height: 130px;
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

.star {
  cursor: pointer;
}
</style>