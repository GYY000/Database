<template>
  <el-row>
    <el-col :span="2">
      <img :src="avatar" style="height: 40px;width: 40px;object-fit: cover;
        display: inline-block;border-radius: 50%; margin-left: 20px"/>
    </el-col>
    <el-col :offset="1" :span="18">
      <el-row v-if="info.type === 'enter'" style="font-size: 17px">
        <span style="font-weight: bold">{{ info.name }}</span> &nbsp join the team.
      </el-row>
      <el-row v-else-if="info.type === 'do_prob'" style="font-size: 17px">
        <span style="font-weight: bold">{{ info.name }}</span> &nbsp
        do the &nbsp <span style="font-weight: bold">{{ info.ques_set_name }}</span>.
      </el-row>
      <el-row v-else style="font-size: 17px">
        <span style="font-weight: bold">{{ info.name }}</span> &nbsp
        create the new set &nbsp <span style="font-weight: bold">{{ info.ques_set_name }}</span>.
      </el-row>
      <el-row>
        {{ info.date }}
      </el-row>
    </el-col>
  </el-row>
</template>

<script>
import {fetch_avatar} from "@/views/main/api";
import {ref} from "vue";

export default {
  name: "history_entry",
  props: ["info"],
  setup(props) {
    const avatar = ref('')

    const init = () => {
      console.log(props.info)
      fetch_avatar(props.info.name).then(
          (res) => {
            avatar.value = res.profile_photo.startsWith('/9j')
                ? 'data:image/jpg;base64,' + res.profile_photo : 'data:image/png;base64,' + res.profile_photo;
          }
      )
    }

    init()

    return {
      avatar,
    }
  }
}
</script>

<style scoped>

</style>