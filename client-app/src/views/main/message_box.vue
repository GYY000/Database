<template>
  <div style="display: flex;flex-direction: column">
    <message v-for="(item,index) in applier_name_list"
             :applier_name="item"
             :team_name="team_name_list[index]"
             :creat_time="time_list[index]"
             :id="id_list[index]">
    </message>
  </div>
</template>

<script>
import userStateStore from "@/store";
import ques_group_card from "@/views/main/question_component/ques_group_card.vue";
import Message from "@/views/main/message_apply/message.vue";

export default {
  name: "message_box",
  components: {Message, ques_group_card},
  props: ["applier_name_list", "team_name_list", "time_list", "id_list"],
  setup(props) {
    const store = userStateStore
    return {
      store
    }
  }
}
</script>

<style scoped>

</style>