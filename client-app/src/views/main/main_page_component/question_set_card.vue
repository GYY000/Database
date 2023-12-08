<template>
    <img :src="avatar" alt="封面"/>
    <div>
        {{ question_set.question_set_name }}
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
  
<style scoped></style>
  