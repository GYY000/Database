<template>
  <el-form>
    <div v-show="image_src !== ''" class="image-container">
      <img :src="image_src" id="show">
    </div>
    <input id="file" type="file"
           accept="image/jpeg,image/png" ref="upload_img"
           @change="show_pic" style="padding-bottom: 15px"/>
    <el-input v-model="set_name" placeholder="请输入问题组的名字"
              clearable style="padding-bottom: 10px" maxlength="15"></el-input>
    <el-input v-model="introduction" placeholder="请输入问题组的简介"
              :autosize="{ minRows: 3, maxRows: 5 }"
              type="textarea"
              clearable maxlength="30"></el-input>
    <div>
      <el-radio-group v-model="is_public" class="ml-4">
        <el-radio label="public" size="large">公有</el-radio>
        <el-radio label="group" size="large">组间共享</el-radio>
      </el-radio-group>
      <el-input v-if="is_public !== 'public'" placeholder="组名" v-model="group_name" clearable
                style="padding-bottom: 15px"></el-input>
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
    const upload_img = ref(null)
    const image_src = ref('')
    const introduction = ref('')

    const closure = () => {
      upload_img.value = ''
      set_name.value = ''
      group_name.value = ''
      image_src.value = ''
      introduction.value = ''
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
      form.append('introduction', introduction.value)
      form.append('set_name', set_name.value)
      form.append('file', upload_img.value.files[0])
      //TODO: 后续可加入tag
      upload_ques_set(form).then(
          (res) => {
            if (res.is_successful === "true") {
              ElMessage({
                message: '上传成功',
                showClose: true,
                type: 'success',
              })
              set_name.value = ''
              group_name.value = ''
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

    const show_pic = (event) => {
      const file = event.target.files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        image_src.value = e.target.result;
      };
      reader.readAsDataURL(file);
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
      add_ques_set,
      upload_img,
      show_pic,
      image_src,
      introduction
    }
  }
}
</script>

<style scoped>
.image-container {
  width: 300px;
  height: 200px;
  overflow: hidden;
  padding-bottom: 10px;
}

.image-container img {
  width: auto;
  height: 100%;
  object-fit: cover;
}
</style>