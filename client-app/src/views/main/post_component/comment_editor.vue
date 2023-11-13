<template>
    <div>
      <!-- 页面内容... -->
  
      <!-- 悬浮输入框 -->
      <div class="fixed-input-container">
        <input type="text" v-model="inputValue" placeholder="在这里输入内容" />
        <button @click="submitForm">发送</button>
      </div>
    </div>
  </template>
  
  <style>
  .fixed-input-container {
    position: fixed;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 80%;
    max-width: 500px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px;
    background-color: #f5f5f5;
  }
  
  .fixed-input-container input {
    flex-grow: 1;
    padding: 10px;
    border: none;
    border-radius: 5px;
  }
  
  .fixed-input-container button {
    margin-left: 10px;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    background-color: #007bff;
    color: #fff;
  }
  </style>
  
  <script>
  import axios from 'axios';
  import userStateStore from "@/store";

  export default {
    data() {
      return {
        inputValue: ''
      };
    },
    methods: {
      submitForm() {
        // 提交表单的逻辑
        // 可以在这里触发绑定的行为
        console.log('提交表单: ' + this.inputValue);
        const store = userStateStore();
        const postData = {
        uid: store.getUserId,
        content: this.inputValue,
        pid: this.$route.params.pid
      };

      axios.post(`/post_detail/${this.$route.params.pid}`, postData)
        .then(response => {
          console.log('接口返回值:', response.data);
          // 在这里处理接口响应
        })
        .catch(error => {
          console.error('接口请求失败:', error);
          // 在这里处理请求失败的情况
        });
      }
    }
  };
  </script>