<template>
    <div>
        <h1>帖子列表</h1>
        <post v-for="post in posts" :key="post.pid" :post="post" />
        <button @click="loadMore">加载更多</button>
    </div>
</template>
  
<script>
import post from "@/views/main/post_component/post.vue";

export default {
    components: {
        post
    },
    data() {
        return {
            posts: [],
            pageNo: 1,
            pageSize: 10
        };
    },
    mounted() {
        this.loadPosts();
    },
    methods: {
        loadPosts() {
            // 发送POST请求，获取帖子数据
            const requestData = {
                page_no: this.pageNo,
                page_size: this.pageSize
            };

            // 假设使用axios发送POST请求，你可以根据你的实际情况选择合适的HTTP库
            axios.post('/post_hub', requestData)
                .then(response => {
                    // 处理返回的帖子数据
                    this.posts = response.data;
                })
                .catch(error => {
                    console.error('加载帖子失败', error);
                });
        },
        loadMore() {
            this.pageNo++; // 加载下一页的帖子数据
            this.loadPosts();
        }
    }
};
</script>
<style scoped></style>