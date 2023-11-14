<template>
  <div style="display: flex;flex-direction: column;">
    <div style="display: flex; justify-content: center">
      <div style="padding-right: 30px">
        <img :src="avatar" style="height: 200px;width: 200px;"/>
      </div>
      <div style="display: flex;flex-direction: column">
        <div class="name_css">{{ team_name }}</div>
        <div style="display: flex;">
          <div style="padding-top: 10px;padding-right: 20px">
            <user_show_card :name="creator" :group_name="team_name" :date="date"></user_show_card>
          </div>
          <div style="display: flex;flex-direction: column">
            <div style="padding-top: 15px;font-size: 15px">创建于</div>
            <div style="padding-top: 10px;font-size: 15px">{{ date }}</div>
          </div>
        </div>
        <div style="padding-top: 10px">
          <!--TODO:-->
          {{ introduction }}
        </div>
      </div>
    </div>
    <div class="user_wrapper">
      <div style="padding-top: 20px;font-size: 25px;color: #409EFF;display: flex;font-family:'Lobster', cursive;justify-content: center">
        Members
      </div>
      <div style="display: flex;justify-content: center;flex-wrap: wrap;padding-top: 5px">
        <div v-if="user_name_list !== null && user_name_list.length !== 0">
          <user_show_card v-for="(item,index) in user_name_list"
                          :name="item"
                          :date="register_date_list[index]"
                          :group_name="team_name"></user_show_card>
        </div>
        <div v-else style="color: #6b778c;font-size: 15px;display: flex;justify-content:center;padding-top: 5px">
          暂时没有用户哦~
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import {fetch_all_member} from "@/views/main/api";
import {ref, watch} from "vue";
import User_show_card from "@/views/main/team_component/user_show_card.vue";

export default {
  name: "edit_team",
  components: {User_show_card},
  props: ['team_name', 'date', 'avatar', 'creator'],
  setup(props) {
    const user_name_list = ref(null)
    const register_date_list = ref(null)
    const introduction = ref('here is supposed to be introduction')

    const init = () => {
      fetch_all_member(props.team_name).then(
          (data) => {
            user_name_list.value = data.name_list
            register_date_list.value = data.register_date_list
          }
      )
    }

    init()

    return {
      user_name_list,
      register_date_list,
      introduction
    }
  }
}
</script>

<style scoped>
.name_css {
  color: #1169ea;
  font-size: 30px;
  font-weight: bold;
}

.user_wrapper{
  display: flex;
  justify-content: center;
  flex-direction: column;
}
</style>