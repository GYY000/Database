<template>
  <el-container style="height: 70vh;">
    <el-container style="height: auto;">
      <el-aside :span="8">
        <h1>
          我的消息 
        </h1>
        <contact v-for="contact in contacts" :key="contact.id" :contact="contact" @open-message="handleContactClicked" />
      </el-aside>
      <el-container>
        <el-main>Main</el-main>
        <el-footer>Footer</el-footer>
      </el-container>
    </el-container>
  </el-container>
</template>
  
<script>
import contact from "@/views/main/site_message_component/contact.vue";
export default {
  name: "message_container",
  components: {
    contact
  },
  data() {
    return {
      contacts: [
        { user_id: 7, user_name: "gyy", has_unread_message: true },
        { user_id: 8, user_name: "zhangjue", has_unread_message: true },
        { user_id: 9, user_name: "wsj", has_unread_message: true }
      ]
    };
  },
  methods: {
    handleContactClicked(contact) {
      // 处理点击联系人的逻辑
      console.log("点击的联系人:", contact);
    }
  }
};
</script>
  
<style scoped>
.el-header,
.el-footer {
  background-color: #B3C0D1;
  color: #333;
  text-align: center;
  line-height: 60px;
}

.el-aside {
  background-color: #D3DCE6;
  color: #333;
  text-align: center;
  line-height: 40px;
}

.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
  line-height: 160px;
}

body>.el-container {
  margin-bottom: 40px;
}

.el-container:nth-child(5) .el-aside,
.el-container:nth-child(6) .el-aside {
  line-height: 260px;
}

.el-container:nth-child(7) .el-aside {
  line-height: 320px;
}
</style>