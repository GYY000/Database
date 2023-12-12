<template>
  <div style="display: flex;justify-content: center">
    <el-form label-width="auto"
        style="left:10%;width: 90%"
    >
      <el-form-item label="题号">
        <el-input v-model.number="form.serial_number" placeholder="请填写题号" clearable/>
      </el-form-item>
      <el-form-item label="分数占比" v-if="form.content.type !== '复合'">
        <el-input v-model.number="form.score" placeholder="请输入题目分数" clearable/>
      </el-form-item>
      <el-form-item label="题目名">
        <el-input v-model.number="form.content.name" placeholder="请输入题目名" clearable/>
      </el-form-item>
      <el-form-item label="题目类型">
        <el-radio-group v-model="form.content.type">
          <el-radio label="选择" name="type"/>
          <el-radio label="填空" name="type"/>
          <el-radio label="问答" name="type"/>
          <el-radio label="复合" name="type"/>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="题目内容"></el-form-item>
      <mavon-editor class="markdown"
                    :value="form.content.ques_content"
                    v-model="form.content.ques_content"
                    :scrollStyle="mavon_config.scrollStyle"
                    :toolbars="mavon_config.toolbars"
                    placeholder="请输入内容"
                    style="height: 200px;width: 90%; left: 5%;margin-bottom: 10px"
                    @imgAdd="img_add"/>
      <el-form-item v-if="form.content.type === '选择'" style="margin-top: 15px">
        <el-button @click="add_ops" :icon="Plus" style="width: 20%;">添加选项</el-button>
      </el-form-item>
      <el-form-item v-if="form.content.type === '选择' && form.content.ops.length !== 0">
        <ques_option v-for="(item,index) in form.content.ops" :index="index" :content=item
                     @upload_op="upload_op" @delete_op="delete_op"
                     style="width:90%;margin-bottom: 5px"></ques_option>
      </el-form-item>
      <el-form-item v-if="form.content.type === '选择'">
        <el-select
            v-model="ops_ans"
            multiple
            placeholder="正确答案"
            style="width: 240px"
        >
          <el-option
              v-for="(item,index) in form.content.ops"
              :key="item"
              :label="String.fromCharCode(index + 65)"
              :value="String.fromCharCode(index + 65)"
          />
        </el-select>
      </el-form-item>
      <el-form-item v-if="form.content.type === '填空'">
        <el-button @click="add_blank" :icon="Plus" style="width: 20%;">添加空格</el-button>
      </el-form-item>
      <div v-if="form.content.type === '填空' && blank_ans.length !== 0">
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
      <el-form-item label="答案" v-if="form.content.type === '问答'"></el-form-item>
      <mavon-editor class="markdown"
                    v-if="form.content.type === '问答'"
                    :value="form.content.ans"
                    v-model="form.content.ans"
                    :scrollStyle="mavon_config.scrollStyle"
                    :toolbars="mavon_config.toolbars"
                    placeholder="请输入您的答案"
                    style="height: 200px;width: 90%; left: 5%;margin-bottom: 10px"
                    @imgAdd="img_add"/>
      <el-form-item v-if="form.content.type==='复合'">
        <el-button @click="add_sub_prob" :icon="Plus" style="width: 20%">添加子问题</el-button>
      </el-form-item>
      <div v-for="(item, index) in form.content.sub_problem" v-if="form.content.type==='复合'">
        <el-form-item :label="`子问题${index + 1}`">
          <el-button @click="open_sub_dialog(index)">查看</el-button>
          <el-button type="danger" @click="delete_sub_prob(index)">删除</el-button>
        </el-form-item>
        <el-dialog v-model="sub_dialog_open[index]" :title="`子问题${index + 1}`" center>
          <sub_prob_form :problem_content="item" :index="index"
                         @upload_sub="upload_sub" @delete_sub_prob="delete_sub_prob"/>
        </el-dialog>
      </div>
    </el-form>
  </div>
  <div style="display: flex;justify-content: center">
    <el-button @click="update(false)"
               type='primary' style="margin-right: 30px">更新</el-button>
    <el-button @click="cancel" type="danger">取消</el-button>
  </div>
</template>

<script>
import {ref} from "vue";
import {api_update_ques, array2String, string2Array, upload_picture} from "@/views/main/api";
import Ques_option from "@/views/quesDoing/ques_option.vue";
import Sub_prob_form from "@/views/quesDoing/sub_prob_form.vue";
import {Plus} from "@element-plus/icons-vue";
import {ElMessage} from "element-plus";
import userStateStore from "@/store";
import router from "@/router";

export default {
  name: 'update_ques_form',
  computed: {
    Plus() {
      return Plus
    }
  },
  props: ["ques", "qs_id"],
  components: {
    Ques_option: Ques_option,
    Sub_prob_form: Sub_prob_form
  },
  setup(props, context) {
    const ops_ans = ref((props.ques.content.type === '选择') ?
                        props.ques.content.ans.split(',') : null)
    const blank_ans = ref((props.ques.content.type === '填空'
        && props.ques.content.type === '填空') ?
        string2Array(props.ques.content.ans) : null)
    const sub_dialog_open = ref(new Array(props.ques.content.sub_problem.length).fill(false))
    const store = userStateStore()

    const form = ref(
        {
          qs_id: props.qs_id,
          creator_id: store.getUserId,
          serial_number: props.ques.serial_num,
          score: props.ques.score,
          content: {
            name: props.ques.content.name,
            ques_content: props.ques.content.ques_content,
            type: props.ques.content.type,
            ops: props.ques.content.ops,
            ans: props.ques.content.ans,
            sub_problem: props.ques.content.sub_problem,
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

    const img_add = (pos, file) => {
      let form_data = new FormData
      form_data.append('image', file)
      upload_picture(form_data).then(
          (res) => {
            let content = form.value.content.ques_content
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
              form.value.content.ques_content = insertStr(str, index, nStr)
            }
          }
      )
    }

    const open_sub_dialog = (index) => {
      sub_dialog_open.value[index] = true
    }

    const upload_sub = (data) => {
      form.value.content.sub_problem[data.index] = data.content
      sub_dialog_open.value[data.index] = false
    }

    const delete_sub_prob = (index) => {
      form.value.content.sub_problem.splice(index, 1)
      sub_dialog_open.value[index] = false
      sub_dialog_open.value.splice(index, 1)
    }

    const add_sub_prob = () => {
      form.value.content.sub_problem.push(
          {
            ques_content: "",
            type: "None",
            ops: [],
            score: 1.0,
            ans: "",
          }
      )
      sub_dialog_open.value.push(true)
    }

    const add_blank = () => {
      blank_ans.value.push("")
    }

    const delete_blank = (index) => {
      blank_ans.value.splice(index, 1)
    }

    const upload_op = (data) => {
      form.value.content.ops[data.index] = data.option
    }

    const delete_op = (index) => {
      form.value.content.ops.splice(index, 1)
    }

    const add_ops = () => {
      form.value.content.ops.push('请填入选项')
    }

    const update = (is_delete) => {
      form.value.content.ans =
          (form.value.content.type === '选择') ? ops_ans.value.join(',') :
              ((form.value.content.type === '填空')?
                  array2String(blank_ans.value) : form.value.content.ans);
      let form1 = {
        is_delete: is_delete,
        qid: props.ques.id,
        serial_num: form.value.serial_number,
        content: form.value.content,
        score: form.value.score
      }
      if(form1.content.type === '复合') {
        form1.score = 0.0
        for(let sub_prob of form.value.content.sub_problem) {
          form1.score = form1.score + sub_prob.score
        }
      }
      api_update_ques(form1).then(
          (res) => {
            if (res.is_successful === "true") {
              ElMessage({
                message: "更新成功",
                type: "success",
              });
              router.go(0)
            } else {
              ElMessage({
                message: "更新失败",
                type: "error",
              });
            }
          }
      )
      context.emit("close_update_form")
    }

    const cancel = () => {
      form.value = {
        serial_number: props.ques.serial_num,
        score: props.ques.score,
        content: {
          name: props.ques.content.name,
          ques_content: props.ques.content.ques_content,
          type: props.ques.content.type,
          ops: props.ques.content.ops,
          ans: props.ques.content.ans,
          sub_problem: props.ques.content.ans,
        }
      }
      context.emit("close_update_form")
    }

    return {
      form,
      mavon_config,
      img_add,
      upload_sub,
      delete_sub_prob,
      add_sub_prob,
      add_ops,
      upload_op,
      delete_op,
      ops_ans,
      blank_ans,
      sub_dialog_open,
      open_sub_dialog,
      update,
      cancel,
      add_blank,
      delete_blank
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