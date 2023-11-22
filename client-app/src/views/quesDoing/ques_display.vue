<template>
  <el-card shadow="never">
    <div style="font-weight: bold; font-size: 20px; display: flex; align-items: center;
    justify-content: space-between;">
      <div>
        {{ ques.serial_num }}.
        {{ content.name }}
        <el-input v-model="score" v-if="edit_score"
                  @keyup.enter.native="update_score" class="score_updater"/>
        <el-button text @click="edit_score = true" v-else class="score_updater">
          {{ score }}
        </el-button>
        分
      </div>
      <el-button :icon="DeleteFilled" type="danger" @click="update_ques(true)" style="margin-right: 50px">
        删除题目
      </el-button>
    </div>
    <div style="display: flex;justify-content: left">
      <!--<v-md-preview :text="content.ques_content" v-if="content_edit === false"
                      @click="content_edit = true"></v-md-preview>-->
      <mavon-editor class="markdown"
                    :value="content.ques_content"
                    v-model="content.ques_content"
                    :scrollStyle="mavon_config.scrollStyle"
                    :box-shadow="false"
                    placeholder="请输入内容"
                    :subfield="false"
                    :toolbars-flag="false"
                    :default-open="content_edit"
                    style="height: auto;min-height:50px;width: 80%;margin-left:30px;margin-bottom: 10px"
                    @imgAdd="img_add"
                    @save="sava_content"
                    @click="content_edit = 'edit'"/>
    </div>
    <div v-for="(item,index) in content.ops"
         style="display: flex;justify-content: left;width: 100%">
      <ques_option v-if="content.type === '选择'"
                   :index="index"
                   :content="item"
                   @delete_op="delete_op"
                   @upload_op="upload_op"
                   style="margin-left:30px; margin-bottom: 10px;width: 80%"></ques_option>
    </div>
    <div style="display: flex;justify-content: left;width: 100%">
      <el-form-item v-if="content.type === '选择'" style="margin-left:30px; margin-bottom: 10px;width: 80%">
        当前答案：
        <el-select
            v-model="ops_ans"
            multiple
            placeholder="正确答案"
            style="width: 240px"
            @change="update_ques(false)"
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
    <div v-if="content.type === '填空'" style="display: flex;justify-content: left;width: 100%">
      <div style="margin-left:30px; margin-bottom: 10px;width: 80%">
        当前答案：
        <el-input v-model="content.ans" v-if="blank_ans_edit"
                  @keyup.enter.native="update_blank_ans"
                  clearable placeholder="请输入正确答案" class="blank_ans"/>
        <el-button text @click="blank_ans_edit = true" v-else class="blank_ans">
          {{ content.ans }}
        </el-button>
      </div>
    </div>
    <div v-if="content.sub_problem.length !== 0"
         style="display: flex;justify-content: left;width: 100%">
      <div style="margin-left:30px; margin-bottom: 10px;width: 80%">
        <div>
          subproblem:
        </div>
      </div>
    </div>
  </el-card>
</template>

<script>
import {ref} from "vue";
import {ElMessage} from "element-plus";
import {api_update_ques, upload_picture} from "@/views/main/api";
import Ques_option from "@/views/quesDoing/ques_option.vue";
import {DeleteFilled} from "@element-plus/icons-vue";

export default {
  name: "ques_display",
  computed: {
    DeleteFilled() {
      return DeleteFilled
    }
  },
  components: {Ques_option},
  props: ["ques", "edit_mode"],

  setup(props, context) {
    const ops_ans = ref((props.ques.content.type === '选择') ?
        props.ques.content.ans.split(',') : null)
    const blank_ans = ref(props.ques.content.ans)
    const blank_ans_edit = ref(false)
    const content_edit = ref("preview")

    const content = ref(
        {
          name: props.ques.content.name,
          ques_content: props.ques.content.ques_content,
          type: props.ques.content.type,
          ops: props.ques.content.ops,
          ans: props.ques.content.ans,
          sub_problem: props.ques.content.sub_problem
        }
    )

    const serial_num = ref(props.ques.serial_num)
    const score = ref(props.ques.score)
    const edit_score = ref(false)

    const update_score = () => {
      edit_score.value = false
      update_ques(false)
    }

    const mavon_config = ref({
          scrollStyle: true
        }
    )

    const img_add = (pos, file) => {
      let form = new FormData
      form.append('image', file)
      upload_picture(form).then(
          (res) => {
            this.$refs.mdedit.$img2Url(pos, res.img_url)
          }
      )
    }

    const update_ques = (is_delete) => {
      content.value.ans =
          (content.value.type === '选择') ? ops_ans.value.join(',') : blank_ans.value;
      let form = {
        is_delete: is_delete,
        qid: props.ques.id,
        serial_num: serial_num.value,
        content: content.value,
        score: score.value
      }
      api_update_ques(form).then(
          (res) => {
            if (res.is_successful === "true") {
              ElMessage({
                message: "更新成功",
                type: "success",
              });
            } else {
              ElMessage({
                message: "更新失败",
                type: "error",
              });
            }
          }
      )
    }

    const delete_op = (index) => {
      content.value.ops.splice(index, 1)
      update_ques(false)
    }

    const upload_op = (data) => {
      content.value.ops[data.index] = data.option
      update_ques(false)
    }

    const update_blank_ans = () => {
      blank_ans_edit.value = false
      update_ques(false)
    }

    const sava_content = (value, render) => {
      content.value.ques_content = value
      content_edit.value = "preview"
      update_ques(false)
    }

    return {
      update_ques,
      content,
      serial_num,
      score,
      update_score,
      edit_score,
      delete_op,
      upload_op,
      ops_ans,
      blank_ans,
      blank_ans_edit,
      update_blank_ans,
      content_edit,
      mavon_config,
      img_add,
      sava_content
    }
  }
}
</script>

<style scoped>
.score_updater {
  width: 8%;
  font-size: 20px;
}

.blank_ans {
  width: 85%
}
</style>