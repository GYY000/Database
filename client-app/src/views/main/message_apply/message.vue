<template>
  <el-card>
    <el-row style="display: flex;">
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
      <div>
        <div style="font-size:17px; padding-bottom: 5px">
          <span style="font-weight: bold;color: #409EFF">{{ applier_name }}</span> 希望加入
          <span style="font-weight: bold;color: #409EFF">{{ team_name }}</span>
        </div>
        <div style="padding-bottom: 15px">
          {{ creat_time }}
        </div>
        <div>
          <el-button type="success" @click="respond_to_apply(true)">
            同意
          </el-button>
          <el-button type="danger" @click="respond_to_apply(false)">
            拒绝
          </el-button>
        </div>
      </div>
    </el-row>

  </el-card>
</template>

<script>
import {fetch_avatar, respond} from "@/views/main/api";
import {ref} from "vue";
import {ElMessage} from "element-plus";
import router from "@/router";

export default {
  name: 'message',
  props: ['id', 'applier_name', 'team_name', 'creat_time'],
  setup(props) {
    const avatar = ref('')
    const flag = ref(true)

    const init = () => {
      fetch_avatar(props.applier_name).then(
          (data) => {
            avatar.value = data.profile_photo.startsWith('/9j')
                ? 'data:image/jpg;base64,' + data.profile_photo : 'data:image/png;base64,' + data.profile_photo;
            flag.value = false
          }
      )
    }

    init()

    const respond_to_apply = (flag) => {
      respond(props.id, props.team_name, props.applier_name, flag).then(
          (res) => {
            if (res.is_successful === 'true') {
              ElMessage({
                message: '完成申请',
                showClose: true,
                type: 'success',
              })
              router.go(0)
            }
          }
      )
    }

    return {
      respond_to_apply,
      avatar,
      flag
    }
  }
}
</script>

<style scoped>

</style>