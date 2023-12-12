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
          <el-radio label="选择" name="type"/>
          <el-radio label="填空" name="type"/>
          <el-radio label="问答" name="type"/>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="题目内容"></el-form-item>
      <mavon-editor class="markdown"
                    v-model="form.ques_content"
                    :value="form.ques_content"
                    :scrollStyle="mavon_config.scrollStyle"
                    :toolbars="mavon_config.toolbars"
                    placeholder="请输入内容"
                    style="height: 100px;width: 85%; left: 10%; margin-bottom: 10px"
                    @imgAdd="img_add_content"/>
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
      <el-form-item v-if="form.type === '填空'">
        <el-button @click="add_blank" :icon="Plus" style="width: 20%;">添加空格</el-button>
      </el-form-item>
      <div v-if="form.type === '填空' && blank_ans.length !== 0">
        <el-form-item v-for="(item,index) in blank_ans" :label="`答案 ${index + 1}`">
          <el-row style="width: 100%">
            <el-col :span="16" style="margin-right: 10px">
              <el-input v-model="blank_ans[index]" placeholder="请填入填空答案"></el-input>
            </el-col>
            <el-col :span="7">
              <el-button type="danger" @click="delete_blank(index)">删除</el-button>
            </el-col>
          </el-row>
        </el-form-item>
      </div>
      <el-form-item label="答案" v-if="form.type === '问答'"></el-form-item>
      <mavon-editor class="markdown"
                    v-if="form.type === '问答'"
                    :value="form.ans"
                    v-model="form.ans"
                    :scrollStyle="mavon_config.scrollStyle"
                    :toolbars="mavon_config.toolbars"
                    placeholder="请输入您的答案"
                    style="height: 200px;width: 90%; left: 5%;margin-bottom: 10px"
                    @imgAdd="img_add_ans"/>
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
import {array2String, string2Array, upload_picture} from "@/views/main/api";

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
    const blank_ans = ref(props.problem_content.ans && props.problem_content.type === '填空' ?
        string2Array(props.problem_content.ans) : [])

    const form = ref(
        {
          ques_content: props.problem_content.ques_content,
          type: props.problem_content.type,
          ops: props.problem_content.ops,
          score: props.problem_content.score,
          ans: props.problem_content.ans,
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

    const add_blank = () => {
      blank_ans.value.push("")
    }

    const delete_blank = (index) => {
      blank_ans.value.splice(index, 1)
    }

    const img_add_content = (pos, file) => {
      let form_data = new FormData
      form_data.append('image', file)
      upload_picture(form_data).then(
          (res) => {
            let content = form.value.ques_content
            let name = file.name
            // 第二步.将返回的url替换到文本原位置![...](0) -> ![...](url)  这里是必须要有的
            if (content.includes(name)) {
              let oStr = `(${pos})`
              let nStr = `(${res.img_url})`
              let index = content.indexOf(oStr)
              let str = content.replace(oStr, '')
              let insertStr = (soure, start, newStr) => {
                return soure.slice(0, start) + newStr + soure.slice(start)
              }
              form.value.ques_content = insertStr(str, index, nStr)
            }
          }
      )
    }

    const img_add_ans = (pos, file) => {
      let form_data = new FormData
      form_data.append('image', file)
      upload_picture(form_data).then(
          (res) => {
            let content = form.value.ans
            let name = file.name
            // 第二步.将返回的url替换到文本原位置![...](0) -> ![...](url)  这里是必须要有的
            if (content.includes(name)) {
              let oStr = `(${pos})`
              let nStr = `(${res.img_url})`
              let index = content.indexOf(oStr)
              let str = content.replace(oStr, '')
              let insertStr = (soure, start, newStr) => {
                return soure.slice(0, start) + newStr + soure.slice(start)
              }
              form.value.ans = insertStr(str, index, nStr)
            }
          }
      )
    }

    const upload_sub_prob = () => {
      form.value.ans = form.value.type === '选择' ? ops_ans.value.join(',') :
          (form.value.type === '填空' ? array2String(blank_ans.value)
              : form.value.ans)
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
      img_add_content,
      img_add_ans,
      delete_sub_prob,
      upload_sub_prob,
      add_blank,
      delete_blank
    }
  }
}
</script>

<style scoped>

</style>