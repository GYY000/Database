<template>
    <div class="set-container">
        <img :src="avatar" alt="封面" class="avatar" />
        <div class="content">
            <router-link :to="'panel_del_index/do_prob/' + question_set.qsid" style="text-decoration: none; color: black;">
                <div style="font-weight: 600;font-size: large;">
                    {{ question_set.question_set_name }}
                </div>
            </router-link>
            <router-link v-if="!question_set.is_public" class="team_name" :to="'/manage_team/' + question_set.tid">
                {{ question_set.team_name }}
            </router-link>
            <div v-else class="team_name">公开题组</div>
        </div>
        <div style="flex-grow: 1;" />
        <div class="time">
            {{ question_set.time }}
        </div>
    </div>
</template>
  
<script>
import axios from 'axios';
export default {
    props: {
        question_set: {
            type: Object,
            required: true,
        },
    },
    data() {
        return {
            avatar: '/src/assets/image/default-avatar.png',
        };
    },
    mounted() {
        this.getAvatar();
    },
    methods: {
        getAvatar() {
            axios.post('/fetch_set_avatar', { set_name: this.question_set.question_set_name })
                .then(response => {
                    this.avatar = response.data.avatar;
                    this.avatar = this.avatar.startsWith('/9j') ? 'data:image/jpg;base64,' + this.avatar
                        : 'data:image/png;base64,' + this.avatar
                })
                .catch(error => {
                    console.error(error);
                });
        },
    },

};
</script>
  
<style scoped>
.set-container {
    display: flex;
    /* 内部组件水平布局 */
    justify-content: flex-start;
    /* 内部组件水平分布 */
    align-items: center;
    /* 垂直居中对齐 */
    height: 50px;
    /* 固定高度 */
    margin: 8px;
    margin-bottom: 20px;
    padding: 0px;
}

.avatar {
    width: 50px;
    /* 图片固定宽度 */
    height: 50px;
    /* 图片固定高度 */
}

.content {
    margin-left: 10px;
    /* 内容离图片的间距 */
    width: 150px;
}

.team_name {
    margin-top: 3px;
    font-size: small;
    font-weight: 300;
    color:rgba(37, 12, 78, 0.881);
}

.time {
    float: right;
    font-size: 12px;
    color: #999;
    padding-top: 20px;
}</style>
  