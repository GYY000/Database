<template>
    <div class="set-container">
        <img :src="avatar" alt="封面" class="avatar" />
        <div class="content">
            <router-link :to="'panel_del_index/do_prob/' + record.qsid" style="text-decoration: none; color: black;">
                <div style="font-weight: 600;font-size: large;">
                    {{ record.question_set_name }}
                </div>
            </router-link>
            <div class="time">
                {{ record.time }}
            </div>
        </div>
        <div style="flex-grow: 1;" />
        <div style="font-size: 20px;font-weight: 800;">
            {{ Number.isInteger(record.user_score) ? record.user_score : record.user_score.toFixed(2) }} 
            / {{ Number.isInteger(record.total_score) ? record.total_score : record.total_score.toFixed(2) }}
        </div>
    </div>
</template>
  
<script>
import axios from 'axios';
export default {
    props: {
        record: {
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
            axios.post('/fetch_set_avatar', { set_name: this.record.question_set_name })
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
    font-size: 14px;
    color: #999;
    margin-top: 5px;
}</style>
  