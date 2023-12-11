<template>
  <el-form style="margin-bottom: 10px">
    <div class="form-label">考试名称</div>
    <el-input v-model="exam_name" placeholder="请输入考试的名字"
              clearable style="padding-bottom: 10px" maxlength="15"></el-input>
    <div class="form-label">问题组名称</div>
    <el-input v-model="ques_set_name" placeholder="请输入所使用问题组名称"
              clearable maxlength="15"></el-input>
    <div class="form-label" style="margin-bottom: 10px;margin-top: 10px">考试时间</div>
    <div>
      <el-row>
        <el-col :span="8">
          <el-date-picker
              v-model="date"
              type="date"
              placeholder="Pick exam date"
              :default-value="new Date()"
          />
        </el-col>
        <el-col :offset="4" :span="8">
          <el-time-picker v-model="time" placeholder="请输入考试时间"
                          format="hh:mm"
                          value-format='HH:mm'/>
        </el-col>
      </el-row>
    </div>
    <div class="form-label" style="margin-bottom: 10px;margin-top: 10px">考试时长</div>
    <el-row>
      <el-col :span="4">
        <el-select v-model="duration_hour" placeholder="小时">
          <el-option
              v-for="number in hourOptions"
              :key="number"
              :value="number"
              :label="number.toString()"
          />
        </el-select>
      </el-col>
      <el-col :span="1" style="font-size: 15px;margin-left: 2px;margin-top: 8px">h</el-col>
      <el-col :span="4">
        <el-select v-model="duration_min" placeholder="小时">
          <el-option
              v-for="number in minOptions"
              :key="number"
              :value="number"
              :label="number.toString()"
          />
        </el-select>
      </el-col>
      <el-col :span="1" style="font-size: 15px;margin-left: 2px;margin-top: 8px">min</el-col>
    </el-row>
  </el-form>
  <div style="display: flex;justify-content: right">
    <el-button @click="closure">Cancel</el-button>
    <el-button type="primary" @click="transmit">
      Confirm
    </el-button>
  </div>

</template>

<script>
import {ref} from "vue";
import userStateStore from "@/store/index";
import {create_exam} from "@/views/main/api";
import {ElMessage} from "element-plus";
import router from "@/router";

export default {
  name: "create_exam_form",
  props: ["dialog_visible"],
  emits: ['change_visible', 'refresh'],

  setup(_, context) {
    const store = userStateStore()
    const exam_name = ref('')
    const ques_set_name = ref('')
    const date = ref(new Date())
    const time = ref(null)
    const duration_min = ref(0)
    const duration_hour = ref(0)
    const hourOptions = ref(Array.from({length: 24}, (_, index) => index))
    const minOptions = ref(Array.from({length: 60}, (_, index) => index))

    const closure = () => {
      exam_name.value = ''
      ques_set_name.value = ''
      date.value = new Date(2023, 12, 11)
      time.value = "00:00"
      duration_min.value = 0
      duration_hour.value = 0
      context.emit('change_visible', false);
    }

    const transmit = () => {
      if(!(date.value.getTime() > new Date().getTime())) {
        ElMessage.error("考试开始时间需要大于当前时间")
        return ;
      }
      const year = date.value.getFullYear();
      const month = String(date.value.getMonth() + 1).padStart(2, '0');
      const day = String(date.value.getDate()).padStart(2, '0');

      const start_time = `${year}-${month}-${day} ${time.value}`;
      create_exam(store.getUserId, start_time, duration_min.value * 60
          + duration_hour.value * 3600, ques_set_name.value, exam_name.value).then(
          (res) => {
            if (res.has_no_perm === 'true') {
              ElMessage.error("您无权使用该问题组创建")
            } else if (res.is_successful === 'false') {
              ElMessage.error("创建失败请稍后再试")
            } else {
              ElMessage.success("成功创建")
              context.emit('change_visible', false);
              context.emit('refresh')
              router.go(0)
            }
          }
      )
    }

    return {
      closure,
      exam_name,
      transmit,
      ques_set_name,
      date,
      time,
      duration_hour,
      duration_min,
      hourOptions,
      minOptions
    }
  }
}
</script>

<style scoped>

</style>

<style>

.form-label {
  font-size: 15px;
  font-weight: bold;
  margin-bottom: 8px;
}
</style>