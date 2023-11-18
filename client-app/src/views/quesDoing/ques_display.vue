<template>
  <div>
    {{ques.content}}
  </div>
</template>

<script>
import {ref} from "vue";

export default {
  name: "ques_display",
  props: ["ques"],

  setup(props, context) {
    const ans = ref(null)

    const upload_ans = () => {
      let ans_form = {ques_id: props.ques.serial_number, ans: ans.value }
      context.emit("upload_ans", ans_form)
    }

    return {
      ans,
      upload_ans
    }
  }
}
</script>

<style scoped>

</style>