<template>
  <img src="src/assets/image/background2.jpg" class="background">
  <div class="secbackground"></div>
  <div class="main_container">
    <div class="title">
      {{store.getQuesGroupName}}
      做题网站
    </div>
    <div>
      <el-pagination

      >

      </el-pagination>
    </div>
  </div>
</template>

<script>
import userStateStore from "@/store";

export default {
  name: 'edit_ques_group',
  setup() {
    const store = userStateStore()
    return {
      store
    }
  }
}
</script>

<style scoped>
.secbackground {
  top: 3%;
  left: 2%;
  width: 96%;
  height: 100vh;
  position: fixed;
  z-index: 0;
  opacity: 90%;
  background-color: #f2f2f2;
}

.background {
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  position: fixed;
  z-index: -1;
  opacity: 30%;
}

.main_container {
  top: 3%;
  left: 5%;
  width: 90%;
  height: 100vh;
}

@font-face {
  font-family: 'YouSheBiaoTiHei';
  src: url('src/assets/fonts/YouSheBiaoTiHei-2.ttf') format('truetype');
}

.title {
  font-family: 'YouSheBiaoTiHei', sans-serif;
  font-size: 50px;
}
</style>