<template>
  <div class="container">
    <el-row>
      <el-col :span="1"></el-col>
      <el-col :span="12">
        <el-card class="vertical">
          <!-- 左边的竖直排列的卡片内容 -->
          <template #header>
            <div class="card-header">
              <h1>欢迎使用WGZForce！</h1>
            </div>
          </template>
          <img src="@/assets/image/welcome.jpg" style="width: 100%;" />
        </el-card>
      </el-col>
      <el-col :span="1"></el-col>
      <el-col :span="8">
        <div class="horizontal-card-container">
          <el-card class="horizontal-card" style="height: 230px;">
            <!-- 右边上方的水平排列的卡片内容 -->
            <template #header>
              <div class="card-header">
                <h2>我的记录</h2>
              </div>
            </template>

          </el-card>
          <el-card class="horizontal-card">
            <!-- 右边下方的水平排列的卡片内容 -->
            <template #header>
              <div class="card-header">
                <h2>最新题集</h2>
              </div>
            </template>
            <div v-for="question_set in recent_question_set" 
              :key="question_set.question_set_name"
              class="question-set"
            >
            </div>
            <question_set_card 
              v-for="question_set in recent_question_set" 
              :key="question_set.question_set_name"
              :question_set="question_set"
            >
            </question_set_card>
          </el-card>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from 'axios';
import userStateStore from "@/store";
import {fetch_set_avatar} from "@/views/main/api";
import question_set_card from './main_page_component/question_set_card.vue';
import Question_set_card from './main_page_component/question_set_card.vue';

export default {
    name: "main_page",
    data() {
        return {
            recent_question_set: [],
            recent_history: []
        };
    },
    mounted() {
        //this.fetch_recent_history();
        this.fetch_recent_question_set();
    },
    methods: {
        fetch_recent_history() {
            const requestData = {
                uid: userStateStore().getUserId,
                total: 4
            };
            axios.post("/get_recent_records", requestData)
                .then(response => {
                this.recent_history = response.data;
                console.log(response.data);
            })
                .catch(error => {
                console.error(error);
            });
        },
        fetch_recent_question_set() {
            const requestData = {
                uid: userStateStore().getUserId,
                total: 4
            };
            axios.post("/get_recent_question_set", requestData)
                .then(response => {
                this.recent_question_set = response.data;
                console.log(response.data);
            })
                .catch(error => {
                console.error(error);
            });
        },
    },
    components: { Question_set_card }
}
</script>

<style scoped>
.container {
  margin: 20px;
}

.vertical-card {
  height: 300px;
}

.card-header {
  display: flex;
  justify-content: center;
  align-items: center;
}

.horizontal-card-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.horizontal-card {
  margin-bottom: 10px;
}

.question-set {
  height: 100px; /* 设置高度为100px，可以根据实际需要调整 */
  width: 100%; /* 宽度占满父组件的宽度 */
  display: flex; /* 内部组件水平布局 */
  justify-content: flex-start; /* 内部组件水平分布 */
}
</style>