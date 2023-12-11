<template>
  <div class="container">
    <el-row>
      <el-col :span="1"></el-col>
      <el-col :span="13">
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
          <el-card class="horizontal-card" style="height: auto;">
            <!-- 右边上方的水平排列的卡片内容 -->
            <template #header>
              <div class="card-header">
                <h2>我的记录</h2>
              </div>
            </template>

            <div v-if="history_waiting_message != ''" style="display: flex;justify-content: center;align-items: center;"> 
              <svg v-if="history_waiting_message == '加载中...'" version="1.1" id="loader-1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                width="30px" height="30px" viewBox="0 0 40 40" enable-background="new 0 0 40 40" xml:space="preserve">
                <path opacity="0.2" fill="#000" d="M20.201,5.169c-8.254,0-14.946,6.692-14.946,14.946c0,8.255,6.692,14.946,14.946,14.946
                  s14.946-6.691,14.946-14.946C35.146,11.861,28.455,5.169,20.201,5.169z M20.201,31.749c-6.425,0-11.634-5.208-11.634-11.634
                  c0-6.425,5.209-11.634,11.634-11.634c6.425,0,11.633,5.209,11.633,11.634C31.834,26.541,26.626,31.749,20.201,31.749z"/>
                <path fill="#000" d="M26.013,10.047l1.654-2.866c-2.198-1.272-4.743-2.012-7.466-2.012h0v3.312h0
                  C22.32,8.481,24.301,9.057,26.013,10.047z">
                  <animateTransform attributeType="xml"
                    attributeName="transform"
                    type="rotate"
                    from="0 20 20"
                    to="360 20 20"
                    dur="0.5s"
                    repeatCount="indefinite"/>
                </path>
              </svg>
              {{ history_waiting_message }} 
            </div>
            <history_card
              v-for="record in recent_history"
              :key="record.question_set_name"
              :record="record"
            >
            </history_card>
          </el-card>
          <el-card class="horizontal-card">
            <!-- 右边下方的水平排列的卡片内容 -->
            <template #header>
              <div class="card-header">
                <h2>最新题集</h2>
              </div>
            </template>

            <div v-if="questionset_waiting_message != ''" style="display: flex;justify-content: center;align-items: center;"> 
              <svg v-if="questionset_waiting_message == '加载中...'" version="1.1" id="loader-1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
                width="30px" height="30px" viewBox="0 0 40 40" enable-background="new 0 0 40 40" xml:space="preserve">
                <path opacity="0.2" fill="#000" d="M20.201,5.169c-8.254,0-14.946,6.692-14.946,14.946c0,8.255,6.692,14.946,14.946,14.946
                  s14.946-6.691,14.946-14.946C35.146,11.861,28.455,5.169,20.201,5.169z M20.201,31.749c-6.425,0-11.634-5.208-11.634-11.634
                  c0-6.425,5.209-11.634,11.634-11.634c6.425,0,11.633,5.209,11.633,11.634C31.834,26.541,26.626,31.749,20.201,31.749z"/>
                <path fill="#000" d="M26.013,10.047l1.654-2.866c-2.198-1.272-4.743-2.012-7.466-2.012h0v3.312h0
                  C22.32,8.481,24.301,9.057,26.013,10.047z">
                  <animateTransform attributeType="xml"
                    attributeName="transform"
                    type="rotate"
                    from="0 20 20"
                    to="360 20 20"
                    dur="0.5s"
                    repeatCount="indefinite"/>
                </path>
              </svg>
              {{ questionset_waiting_message }} 
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
import question_set_card from './main_page_component/question_set_card.vue';
import history_card from './main_page_component/history_card.vue';

export default {
    name: "main_page",
    data() {
        return {
            recent_question_set: [],
            recent_history: [],
            history_waiting_message: "加载中...",
            questionset_waiting_message: "加载中..."
        };
    },
    mounted() {
        this.fetch_recent_history();
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
                if (this.recent_history.length == 0) {
                  this.history_waiting_message = "你当前没有做题记录";
                } else {
                  this.history_waiting_message = "";
                }
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
                if (this.recent_question_set.length == 0) {
                  this.questionset_waiting_message = "当前没有可查看的题集";
                } else {
                  this.questionset_waiting_message = "";
                }
            })
                .catch(error => {
                console.error(error);
            });
        },
    },
    components: { question_set_card, history_card }
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