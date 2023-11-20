<template>
  <el-card shadow="never">
    <div style="display: flex;justify-content: left">
      <el-row>
        <el-col style="width:15%">
          {{ ques.serial_num }}.
        </el-col>
        <el-col>
          <v-md-preview :text="ques.content.ques_content"></v-md-preview>
        </el-col>
      </el-row>
      <el-row v-if="ques.content.type === '选择'">

      </el-row>
      <el-row></el-row>
    </div>
  </el-card>
</template>

<script>
import {ref} from "vue";

export default {
  name: "ques_display",
  props: ["ques", "edit_mode"],

  setup(props, context) {
    const ans = ref(null)
    const ques = ref(
        {

        }
    )

    const update_ques = () => {

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