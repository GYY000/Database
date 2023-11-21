<template>
  <div style="display: flex;justify-content: center">
    <el-form
        label-width="auto"
        style="left:10%;width: 90%"
    >
      <el-form-item label="分数占比">
        <el-input v-model.number="form.score" placeholder="请输入题目分数" clearable/>
      </el-form-item>
      <el-form-item label="题目类型">
        <el-radio-group v-model="form.type">
          <el-radio label="None" name="type"/>
          <el-radio label="选择" name="type"/>
          <el-radio label="填空" name="type"/>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="题目内容"></el-form-item>
      <mavon-editor class="markdown"
                    v-model="form.ques_content"
                    :scrollStyle="mavon_config.scrollStyle"
                    :toolbars="mavon_config.toolbars"
                    placeholder="请输入内容"
                    style="height: 100px;width: 85%; left: 10%; margin-bottom: 10px"
                    @imgAdd="img_add"/>
      <el-form-item v-if="form.type === '选择'" style="margin-top: 15px">
        <el-button @click="add_ops" :icon="Plus" style="width: 20%;">添加选项</el-button>
      </el-form-item>
      <el-form-item v-if="form.type === '选择'">
        <ques_option v-for="(item,index) in form.ops" :index="index" :content=item
                     @upload_op="upload_op" @delete_op="delete_op"
                     style="width:90%;margin-bottom: 5px"></ques_option>
      </el-form-item>
      <el-form-item v-if="form.type === '选择'">
        <el-select
            v-model="ops_ans"
            multiple
            placeholder="正确答案"
            style="width: 240px"
        >
          <el-option
              v-for="(item,index) in form.ops"
              :key="item"
              :label="String.fromCharCode(index + 65)"
              :value="String.fromCharCode(index + 65)"
          />
        </el-select>
      </el-form-item>
      <el-form-item v-if="form.type === '填空'" label="答案">
        <el-input v-model="blank_ans"></el-input>
      </el-form-item>
    </el-form>
  </div>
  <div style="display: flex;width: 100%;justify-content: center;padding-top: 10px">
    <el-button @click="upload_sub_prob" style="margin-right: 20px">保存</el-button>
    <el-button @click="delete_sub_prob" type="danger">删除</el-button>
  </div>
</template>

<script>
import Ques_option from "@/views/quesDoing/ques_option.vue";
import {ref} from "vue";
import {Plus} from "@element-plus/icons-vue";
import {upload_picture} from "@/views/main/api";

export default {
  name: 'sub_prob_form',
  computed: {
    Plus() {
      return Plus
    }
  },
  components: {Ques_option},
  props: ['index', 'problem_content'],
  setup(props, context) {
    const ops_ans = ref(props.problem_content.ans ? props.problem_content.ans.split(',') : [])
    const blank_ans = ref(props.problem_content.ans)

    const form = ref(
        {
          ques_content: props.problem_content.ques_content,
          type: props.problem_content.type,
          ops: props.problem_content.ops,
          score: props.problem_content.score,
          ans: [],
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

    const upload_op = (data) => {
      form.value.ops[data.index] = data.option
    }

    const delete_op = (index) => {
      form.value.ops.splice(index, 1)
    }

    const add_ops = () => {
      form.value.ops.push('请填入选项')
    }

    const img_add = (pos, file) => {
      let form = new FormData
      form.append('image', file)
      upload_picture(form).then(
          (res) => {
            this.$refs.mdedit.$img2Url(pos, res.img_url)
          }
      )
    }

    const upload_sub_prob = () => {
      form.value.ans = form.value.type === '选择' ? ops_ans.value.join(',') : blank_ans
      context.emit('upload_sub', {index: props.index, content: form.value})
    }

    const delete_sub_prob = () => {
      context.emit('delete_sub_prob', props.index)
    }

    return {
      form,
      mavon_config,
      ops_ans,
      blank_ans,
      upload_op,
      add_ops,
      delete_op,
      img_add,
      delete_sub_prob,
      upload_sub_prob
    }
  }
}
</script>

<style scoped>

</style>