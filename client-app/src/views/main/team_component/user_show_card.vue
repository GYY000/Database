<template>
  <!-- TODO:也许有时间可以做一个悬浮效果-->
  <button @click="show_info = true">
    <el-skeleton :loading="flag" animated>
      <template #template>
        <el-skeleton-item variant="image" style="height: 40px;width: 40px;border-radius: 50%"/>
      </template>
      <template #default>
        <img :src="avatar" style="height: 40px;width: 40px;border-radius: 50%"/>
      </template>
    </el-skeleton>
  </button>

  <el-dialog v-model="show_info">
    <el-card>
      <div style="display: flex; flex-direction: column">
        <div style="padding-right: 20px">
          <el-skeleton :loading="flag" animated>
            <template #template>
              <el-skeleton-item variant="image" style="width: 100px; height: 100px; border-radius: 50%"/>
            </template>
            <template #default>
              <img :src="avatar" style="width: 100px; height: 100px;border-radius: 50%">
            </template>
          </el-skeleton>
        </div>
        <div style="font-size:17px; padding-bottom: 5px;display: flex;justify-content: center">
          <span style="font-weight: bold;color: #409EFF">{{ name }}</span>
        </div>
        <div style="padding-bottom: 15px;display: flex;justify-content: center">
          加入于 {{ date }}
        </div>
        <div>
          <el-button type="danger" @click="del_mem">
            删除
          </el-button>
        </div>
      </div>
    </el-card>
  </el-dialog>
</template>

<script>

import {del_member, fetch_avatar} from "@/views/main/api";
import {ref} from "vue";
import {ElMessage} from "element-plus";

export default {
  name: "user_show_card",
  props: ['name', 'date', 'group_name'],
  setup(props) {
    const avatar = ref('')
    const show_info = ref(false)
    const flag = ref(true)

    const init = () => {
      fetch_avatar(props.name).then(
          (data) => {
            avatar.value = data.profile_photo.startsWith('/9j')
                ? 'data:image/jpg;base64,' + data.profile_photo : 'data:image/png;base64,' + data.profile_photo;
            flag.value = false
          }
      )
    }

    const del_mem = () => {
      del_member(props.name, props.group_name).then(
          (res) => {
            if (res.is_successful === 'true') {
              ElMessage({
                message: '删除用户',
                showClose: true,
                type: 'error',
              })
            }
          }
      )
    }
    init()
    return {
      avatar,
      del_mem,
      show_info,
      flag
    }
  }
}

</script>

<style scoped>

</style>