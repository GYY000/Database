<template>
  <el-form label-width="120px">
    <el-form-item label="题号">
      <el-input v-model.number="form.serial_number" placeholder="请填写题号" clearable/>
    </el-form-item>
    <el-form-item label="分数占比">
      <el-input v-model.number="form.serial_number" placeholder="请输入题目分数" clearable/>
    </el-form-item>
    <el-form-item label="题目类型">
      <el-checkbox-group v-model="form.content.type">
        <el-checkbox label="None" name="type"/>
        <el-checkbox label="选择" name="type"/>
        <el-checkbox label="填空" name="type"/>
      </el-checkbox-group>
    </el-form-item>
    <el-form-item label="题目内容">
      <mavon-editor style="height: 200px"></mavon-editor>
    </el-form-item>
  </el-form>
</template>

<script>
import {ref} from "vue";
import MavonEditor from "mavon-editor/src/mavon-editor.vue";

export default {
  name: 'upload_ques_form',
  components: {MavonEditor},
  setup() {
    const form = ref(
        {
          serial_number: 1,
          score: 1.0,
          content: {
            name: "",
            ques_content: "",
            type: "None",
            ops: {},
            ans: "",
            sub_problem: []
          }
        }
    )
    return {
      form
    }
  }
}
</script>

<style scoped>

</style>