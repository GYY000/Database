<template>
  <el-row style="margin-bottom: 5px;margin-left: 30px">
    <el-col>
      <el-tag class="mx-1" size="default" v-if="content.type === '选择'">选择题</el-tag>
      <el-tag class="mx-1" size="default" v-if="content.type === '填空'">填空题</el-tag>
      <el-tag class="mx-1" size="default" v-if="content.type === '问答'">问答题</el-tag>
      <el-tag class="mx-1" size="default" :type="'success'" style="margin-left: 10px">{{ content.score }}分</el-tag>
    </el-col>
  </el-row>
  <el-row>
    <el-col :span="22">
      <v-md-preview :text="content.ques_content"></v-md-preview>
    </el-col>
  </el-row>
  <div v-if="content.type === '选择'" style=";margin-left: 30px">
    <el-checkbox-group v-model="ans" v-for="(item,index) in content.ops" size="small">
      <el-row>
        <el-checkbox size="large" :label="String.fromCharCode(index + 65) + '.' + item"
                     style="width: 90%; margin-bottom: 10px" border disabled/>
      </el-row>
    </el-checkbox-group>
    <el-form-item v-if="content.type === '选择'"
                  style="margin-bottom: 10px;width: 80%">
      <el-tag size="large" style="margin-right: 20px" effect="dark">答案</el-tag>
      <el-select
          v-model="ans"
          multiple
          placeholder="正确答案"
          style="width: 240px"
          disabled
      >
        <el-option
            v-for="(item,index) in content.ops"
            :key="item"
            :label="String.fromCharCode(index + 65)"
            :value="String.fromCharCode(index + 65)"
        />
      </el-select>
    </el-form-item>
  </div>
  <div v-if="content.type === '填空'" style="margin-left: 30px">
    <div style="margin-bottom: 10px">
      <el-tag size="large" effect="dark">答案Demo</el-tag>
    </div>
    <el-form style="margin-bottom: 10px;width: 80%" label-width="auto">
      <div v-for="(item,index) in ans">
        <el-form-item :label="`空格 ${index + 1}`">
          <el-input :value="ans[index]" disabled></el-input>
        </el-form-item>
      </div>
    </el-form>
  </div>
  <div v-if="content.type === '问答'" style="margin-bottom: 10px;margin-left: 30px">
    <div style="margin-bottom: 10px">
      <el-tag size="large" effect="dark">答案Demo</el-tag>
    </div>
    <mavon-editor :box-shadow="true" :default-open="'preview'" :editable="false"
                  :toolbars-flag="false" :subfield="false" style="min-width: 0; width:60%;min-height: 200px"
                  :value="ans" v-model="ans">
    </mavon-editor>
  </div>
</template>

<script>
import {ref} from "vue";
import Ques_option from "@/views/quesDoing/ques_option.vue";
import {DeleteFilled, Edit} from "@element-plus/icons-vue";
import Update_ques_form from "@/views/quesDoing/update_ques_form.vue";
import {string2Array} from "@/views/main/api";

export default {
  name: "sub_problem_do",
  computed: {
    Edit() {
      return Edit
    },
    DeleteFilled() {
      return DeleteFilled
    }
  },
  components: {Update_ques_form, Ques_option},
  props: ["sub_problem", "id"],

  setup(props) {
    const ans = ref((props.sub_problem.type === '选择') ?
        props.sub_problem.ans.split(',') :
        ((props.sub_problem.type === '填空') ?
            string2Array(props.sub_problem.ans) :
            props.sub_problem.ans))

    const content = ref(
        {
          ques_content: "**（" + (props.id + 1) + "）** " + props.sub_problem.ques_content,
          type: props.sub_problem.type,
          ops: props.sub_problem.ops,
          score: props.sub_problem.score
        }
    )
    return {
      content,
      ans,
    }
  }
}
</script>

<style scoped>

</style>