<template>
  <el-form>
    <input type="file" accept="image/jpeg,image/png" ref="upload_image"/>
    <el-input v-model="set_name" placeholder="请输入用户组的名字"></el-input>
    <div>
      <el-radio-group v-model="is_public" class="ml-4">
        <el-radio label="public" size="large">公有</el-radio>
        <el-radio label="group" size="large">组间共享</el-radio>
      </el-radio-group>
      <el-input v-if="is_public !== 'public'" placeholder="组名" v-model="group_name"></el-input>
    </div>
  </el-form>
  <el-button @click="closure">Cancel</el-button>
  <el-button type="primary" @click="transmit">
    Confirm
  </el-button>
</template>

<script>
import {ref} from "vue";
import userStateStore from "@/store/index";
import {check_inside_group, upload_ques_set} from "@/views/main/api";
import {ElMessage} from "element-plus";

export default {
  name: "create_ques_group",
  props: ["dialog_visible"],
  setup(_, context) {
    const store = userStateStore()
    const is_public = ref('public')
    const group_name = ref('none')
    const set_name = ref('')

    const closure = () => {
      context.emit('change_visible', false);
    }
    const add_ques_set = () => {
      let form = new FormData
      form.append("user_id", store.getUserId)
      if (is_public === 'group') {
        form.append("group_name", group_name.value)
      } else {
        form.append("group_name", 'none')
      }
      form.append('set_name', set_name.value)
      form.append('file', this.$refs.upload_image.files[0])
      //TODO: 后续可加入tag
      upload_ques_set(form).then(
          (res) => {
            if (res.is_successful === "true") {
              ElMessage({
                message: '上传成功',
                showClose: true,
                type: 'success',
              })
            } else {
              ElMessage({
                message: '上传失败，请稍后再试',
                showClose: true,
                type: 'error',
              })
            }
          }
      )
    }

    const transmit = () => {
      if (is_public.value === 'public') {
        add_ques_set()
        closure()
      } else {
        const data = {
          user_name: store.getUserName,
          group_name: group_name.value
        }
        const boolean = ref(false)
        check_inside_group(data).then(
            (res) => {
              boolean.value = res.is_inside === "true"
            }
        ).then(
            () => {
              if (boolean.value) {
                add_ques_set()
                closure()
              } else {
                ElMessage({
                  message: '您不在用户组内，请重新确认',
                  showClose: true,
                  type: 'error',
                })
              }
            }
        )
      }
    }
    return {
      closure,
      is_public,
      group_name,
      transmit,
      set_name,
      add_ques_set
    }
  }
}
</script>

<style scoped>

</style>