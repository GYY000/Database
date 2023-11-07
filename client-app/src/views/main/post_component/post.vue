<template>
  <div class="post">
    <h2>{{ post.title }}</h2>
    <p>{{ post.content }}</p>
    <p>作者：{{ post.creator_name }}</p>
    <p>更新时间：{{ post.update_time }}</p>
    <img :src="post.profile_photo" alt="头像" />
  </div>
</template>
  
<script>
export default {
  props: {
    post: {
      type: Object,
      required: true,
    },
  },
};
</script>
  
  <style scoped>
.post {
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
}
</style>