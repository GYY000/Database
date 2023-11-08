<template>
  <el-card shadow="hover">
    <div class="card_layout">
      <div class="l_column">
        <div class="image-container">
          <img :src="img_url" alt="can't find the jpg">
        </div>
      </div>
      <div class="r_column">
        <div class="set_title">{{set_name}}</div>
        <div class="set_content">
          <span>{{creator_name}}</span>
          <span>created at {{date}}</span>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script>
import {ref} from "vue";

export default {
  name: "ques_group_card",
  props: ['creator_name', 'set_name','avatar','date'],
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
}

.l_column {
  flex-grow: 3;
}

.r_column {
  flex-grow: 2;
}

.image-container {
  width: 300px; /* 指定容器的宽度 */
  height: 200px; /* 指定容器的高度 */
  overflow: hidden; /* 裁剪超出容器的部分 */
}

.image-container img {
  width: auto;
  height: 100%;
  object-fit: cover; /* 缩放图片以填充容器，并裁剪超出的部分 */
}

.set_title{
  font-size: 35px;
  color: #1169ea;
}
.set_content{
  font-size: 15px;
  color: #6b778c;
}
</style>