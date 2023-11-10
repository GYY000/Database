<template>
  <div style="display: flex;flex-direction: column">
    <div style="display: flex; justify-content: center">
      <div>
        <img :src="avatar" style="height: 200px;width: 200px;"/>
      </div>
      <div>

      </div>
    </div>
    <div style="font-size: 20px;color: #409EFF">
      组内用户
    </div>
    <div style="display: flex;justify-content: left;flex-wrap: wrap">
      <user_show_card v-for="(item,index) in user_names"
                      :name="item"
                      :date="register_date_list[index]"
                      :group_name="team_name"></user_show_card>
    </div>
  </div>
</template>

<script>
import {fetch_all_member} from "@/views/main/api";
import {ref} from "vue";
import User_show_card from "@/views/main/team_component/user_show_card.vue";

export default {
  name: "edit_team",
  components: {User_show_card},
  props: ['team_name', 'date', 'avatar'],
  setup(props) {
    const user_names = ref(null)
    const register_date_list = ref(null)

    const init = () => {
      fetch_all_member(props.team_name).then(
          (data) => {
            user_names.value = data.name_list
            register_date_list.value = data.register_date_list
          }
      )
    }

    init()

    return {
      user_names,
      register_date_list,
    }
  }
}
</script>

<style scoped>

</style>