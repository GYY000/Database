<template>
  <el-card style="width: 100%">
    <el-tag style="margin-right: 10px;">{{op}}</el-tag>
    <el-input v-if="edit_mode === true"
              placeholder="请输入选项名"
              v-model="edit_content" @keyup.enter.native="upload_op" style="width: 70%;height:60%"></el-input>
    <div v-else @click="change_edit(true)" style="width: 70%;height:60%;display: inline-block">{{content}}</div>
    <el-button @click="delete_op" type="danger"
               style="margin-left:10px;height:60%;width: 15%; right: 5%">删除</el-button>
  </el-card>
</template>

<script>
  import {ref} from "vue";

  export default {
    name: "ques_option",
    props: ["index", "content"],
    setup(props, context) {
      const op = ref(String.fromCharCode(props.index + 65))
      const edit_mode = ref(false)
      const edit_content = ref(props.content)

      const upload_op = () => {
        let data = {'index':props.index, 'option' : edit_content.value}
        context.emit("upload_op", data)
        edit_mode.value = false
      }

      const delete_op = () => {
        context.emit("delete_op", props.index)
      }

      const change_edit = (flag) => {
        edit_mode.value = flag
      }

      return {
        op,
        edit_mode,
        edit_content,
        upload_op,
        change_edit,
        delete_op
      }
    }
  }
</script>

<style scoped>

</style>