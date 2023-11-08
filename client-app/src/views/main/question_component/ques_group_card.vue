<template>
  <el-card shadow="hover">
    <div class="card_layout">
      <div class="l_column">
        <div class="image-container">
          <img :src="img_url" alt="can't find the jpg">
        </div>
      </div>
      <div class="r_column">
        <div class="set_title">
          {{ set_name }}
          <div class="seperator"></div>
        </div>
        <div class="set_content">
          这里是代做的简介
        </div>
        <div class="set_create">
          <span>{{ creator_name }}</span>
          <span> created at {{ date }}</span>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script>
import {ref} from "vue";

export default {
  name: "ques_group_card",
  props: ['creator_name', 'set_name', 'avatar', 'date'],
  setup(props) {
    const img_url = ref(props.avatar.startsWith('/9j')
        ? 'data:image/jpg;base64,' + props.avatar : 'data:image/png;base64,' + props.avatar);
    return {
      img_url
    }
  }
}
</script>

<style scoped>
.card_layout {
  display: flex;
  max-width: 400px;
}

.l_column {
  flex-grow: 2;
  max-width: 300px;
}

.r_column {
  flex-grow: 3;
}

.image-container {
  width: 225px; /* 指定容器的宽度 */
  height: 200px; /* 指定容器的高度 */
  overflow: hidden; /* 裁剪超出容器的部分 */
}

.image-container img {
  width: 200px;
  height: 200px;
  object-fit: cover;
}

.set_title {
  font-weight: bold;
  font-size: 25px;
  color: #1169ea;
  height: 30%;
}

.set_content {
  height: 50%;
}

.set_create {
  font-size: 15px;
  color: #6b778c;
  height: 20%;
}

.seperator {
  height: 1px;
  width: 80%;
  position: relative;
  margin-top: 5px;
  background: linear-gradient(to bottom right, rgba(214, 216, 220, 0.96) 0%,
  rgba(70, 64, 255, 0.56) 60%,
  rgba(214, 216, 220, 0.96) 100%);
  box-shadow: 0px -2px 4px rgba(0, 0, 0, 0.2);
}
</style>