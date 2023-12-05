<template>
  <div @click="show_info = true">
    <el-skeleton :loading="flag" animated>
      <template #template>
        <el-skeleton-item variant="image" style="height: 60px;width: 60px;border-radius: 50%"/>
      </template>
      <template #default>
        <img :src="avatar" style="height: 60px;width: 60px;border-radius: 50%"/>
      </template>
    </el-skeleton>
  </div>

  <el-dialog v-model="show_info" style="width:400px" draggable>
    <div style="display: flex;justify-content: center">
      <div>
        <el-skeleton :loading="flag" animated>
          <template #template>
            <el-skeleton-item variant="image" style="width: 100px; height: 100px; border-radius: 50%"/>
          </template>
          <template #default>
            <img :src="avatar" style="width: 100px; height: 100px;border-radius: 50%">
          </template>
        </el-skeleton>
      </div>
      <div style="display: flex; flex-direction: column;padding-left: 20px">
        <div style="font-size:17px; padding-bottom: 5px;display: flex;justify-content: left">
          <span style="font-weight: bold;color: #409EFF">{{ name }}</span>
        </div>
        <div style="padding-bottom: 15px;display: flex;justify-content: center">
          加入于 {{ date }}
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script>

import {fetch_avatar} from "@/views/main/api";
import {ref} from "vue";

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

    init()
    return {
      avatar,
      show_info,
      flag
    }
  }
}

</script>

<style scoped>

</style>