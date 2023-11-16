<template>
  <el-form label-width="120px">
    <el-form-item label="题号">
      <el-input v-model.number="form.serial_number" placeholder="请填写题号" clearable/>
    </el-form-item>
    <el-form-item label="分数占比">
      <el-input v-model.number="form.serial_number" placeholder="请输入题目分数" clearable/>
    </el-form-item>
    <el-form-item label="题目类型">
      <el-radio-group v-model="form.content.type">
        <el-radio label="None" name="type"/>
        <el-radio label="选择" name="type"/>
        <el-radio label="填空" name="type"/>
      </el-radio-group>
    </el-form-item>

  </el-form>
  <div class="editor">
    <mavon-editor class="markdown"
     :value="mark_data"
     :subfield = "mavon_config.subfield"
     :defaultOpen = "mavon_config.defaultOpen"
     :toolbarsFlag = "mavon_config.toolbarsFlag"
     :editable="mavon_config.editable"
     :scrollStyle="mavon_config.scrollStyle">
    </mavon-editor>
  </div>
</template>

<script>
import {ref} from "vue";

export default {
  name: 'upload_ques_form',
  components: ["mavonEditor"],
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

    const mavon_config = ref({
          subfield: false,// 单双栏模式
          defaultOpen: 'preview',//edit： 默认展示编辑区域 ， preview： 默认展示预览区域
          editable: false,
          toolbarsFlag: false,
          scrollStyle: true
        })

    const mark_data = ref("**wsj**")
    return {
      form,
      mavon_config,
      mark_data
    }
  }
}
</script>

<style scoped>
.editor {
  margin: auto;
  width: 80%;
  height: 580px;
}
</style>