<template>
  <div>
    <el-tabs @tab-change="change_tab" class="tabs">
      <!--- TODO -->
      <el-tab-pane label="主页" name="/main_page">
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component"/>
          </keep-alive>
        </router-view>
      </el-tab-pane>
      <el-tab-pane label="题目广场" name="/question_hub">
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component"/>
          </keep-alive>
        </router-view>
      </el-tab-pane>
    </el-tabs>
  </div>
  <div class="r-container">
    <el-button v-if="is_login" @click="logout" type="primary" :icon="SortDown" class="button">
      Logout
    </el-button>
    <el-button v-else @click="login" type="primary" :icon="SortUp" class="button">
      Login
    </el-button>
    <el-button @click="change_tab('/user_center')" type="primary" :icon="User" class="button"></el-button>
  </div>
</template>

<style scoped>
.tabs {
  position: fixed;
  top: 5%;
  left: 5%;
  right: 5%;
  bottom: 5%;
  width: 87%;
}

.button {

}

.r-container {
  position: fixed;
  top: 5%;
  right: 5%;
}
</style>

<script>
import {SortDown, SortUp, User} from '@element-plus/icons-vue'
import {ref} from "vue";
import router from "@/router";
import store from "@/store";

export default {
  name: "index",
  setup() {
    const is_login = ref(store.getters.getIsAuthentic);
    const tab_path = ref("user_page");

    const change_tab = (name) => {
      tab_path.value = name;
      router.push(tab_path.value);
    };

    const logout = () => {
      store.dispatch("logout", {});
      router.push({path: '/login'});
    };

    const login = () => {
      router.push({path: '/login'});
    };

    return {
      is_login,
      tab_path,
      change_tab,
      logout,
      login
    };
  },
  computed: {
    User() {
      return User;
    },
    SortUp() {
      return SortUp;
    },
    SortDown() {
      return SortDown;
    },
  },
}
</script>