<template>
  <el-card shadow="hover" style="width:30%; border-radius: 3%;margin-top: 10px">
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
          这里是待做的简介
        </div>
        <div class="set_create">
          <div style="padding: 2px">{{ creator_name }} created at</div>
          <div>{{ date }}</div>
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
  width: 150px; /* 指定容器的宽度 */
  height: 130px; /* 指定容器的高度 */
  overflow: hidden; /* 裁剪超出容器的部分 */
}

.image-container img {
  width: 130px;
  height: 130px;
  object-fit: cover;
}

.set_title {
  font-weight: bold;
  font-size: 18px;
  color: #1169ea;
  height: 30%;
}

.set_content {
  height: 50%;
  font-size: 10px;
}

.set_create {
  font-size: 10px;
  color: rgb(86, 94, 108);
  height: 20%;
}

.seperator {
  height: 1px;
  width: 90%;
  position: relative;
  margin-top: 5px;
  background: linear-gradient(to bottom right, rgba(214, 216, 220, 0.96) 0%,
  rgba(70, 64, 255, 0.56) 60%,
  rgba(214, 216, 220, 0.96) 100%);
  box-shadow: 0px -2px 4px rgba(0, 0, 0, 0.2);
}
</style>