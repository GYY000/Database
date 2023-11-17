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
    <el-form-item label="题目内容"></el-form-item>
      <mavon-editor class="markdown"
                    v-model="form.content.ques_content"
                    :scrollStyle="mavon_config.scrollStyle"
                    :toolbars="mavon_config.toolbars"
                    placeholder="请输入内容"
                    style="height: 200px"
                    @imgAdd="img_add"/>
  </el-form>
</template>

<script>
import {ref} from "vue";
import {upload_picture, upload_team} from "@/views/main/api";
import {ElMessage} from "element-plus";

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
          scrollStyle: true,
          toolbars: {
            bold: true, // 粗体
            italic: true, // 斜体
            header: true, // 标题
            underline: true, // 下划线
            strikethrough: false, // 中划线
            mark: false, // 标记
            superscript: true, // 上角标
            subscript: true, // 下角标
            quote: true, // 引用
            ol: true, // 有序列表
            ul: true, // 无序列表
            link: true, // 链接
            imagelink: true, // 图片链接
            code: true, // code
            table: true, // 表格
            fullscreen: false, // 全屏编辑
            readmodel: false, // 沉浸式阅读
            htmlcode: false, // 展示html源码
            help: false, // 帮助
            undo: true, // 上一步
            redo: true, // 下一步
            trash: true, // 清空
            save: true, // 保存（触发events中的save事件）
            navigation: false, // 导航目录
            alignleft: true, // 左对齐
            aligncenter: true, // 居中
            alignright: true, // 右对齐
            subfield: true, // 单双栏模式
            preview: true, // 预览
          }
        }
    )

    const img_add= (pos, file) => {
      let form = new FormData
      form.append('image', file)
      upload_picture(form).then(
          (res) => {
            this.$refs.mdedit.$img2Url(pos,res.img_url)
          }
      )
    }

    const mark_data = ref("**wsj**")
    return {
      form,
      mavon_config,
      mark_data,
      img_add
    }
  }
}
</script>

<style scoped>
.editor {
  margin: auto;
  width: 90%;
  height: 580px;
}
</style>