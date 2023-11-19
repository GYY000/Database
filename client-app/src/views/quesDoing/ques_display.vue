<template>
  <el-card shadow="never">
    <div style="display: flex;justify-content: left">
      <el-col style="width:15%">
        {{ques.serial_num}}.
      </el-col>
      <el-col>
        <v-md-preview :text="ques.content.ques_content"></v-md-preview>
      </el-col>
    </div>

  </el-card>
</template>

<script>
import {ref} from "vue";

export default {
  name: "ques_display",
  props: ["ques","edit_mode"],

  setup(props, context) {
    const ans = ref(null)

    const upload_ans = () => {
      let ans_form = {ques_id: props.ques.serial_number, ans: ans.value }
      context.emit("upload_ans", ans_form)
    }

    const init = () => {
      console.log("content")
      console.log(props.ques.content)
    }

    init()

    return {
      ans,
      upload_ans
    }
  }
}
</script>

<style scoped>

</style>