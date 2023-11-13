<template>
  <div>
    <h1>asdfgh</h1>
    <p>{{ post.content }}</p>
    <p>1231231</p>
    <comment
      v-for="comment in comments"
      :key="comment.cid"
      :comment="comment"
    />
    <comment_editor></comment_editor>
  </div>
</template>
  
<script>
import comment from "@/views/main/post_component/comment.vue";
import comment_editor from "@/views/main/post_component/comment_editor.vue";
import axios from "axios";
export default {
  name: "post_detail",
  components: {
    comment,
    comment_editor,
  },
  data() {
    return {
      post: {},
      comments: [],
    };
  },
  mounted() {
    // 在组件挂载后通过API请求获取帖子详情数据
    console.log("挂钩")
    this.fetchPostDetail();
  },
  methods: {
    fetchPostDetail() {
        // 获取路由参数中的pid
        const pid = this.$route.params.pid;
        axios.get(`/post_detail/${pid}`)
            .then((response) => {
            this.post = response.data.post;
            this.comments = response.data.comment;
            })
            .catch((error) => {
            console.error(error);
            });
        }
  },
};
</script>
<style scoped></style>