<template>
  <img src="src/assets/image/background2.jpg" class="background">
  <div class="secbackground"></div>

</template>

<script>
export default {
  name: 'edit_ques_group',
  setup() {

  }
}
</script>

<style scoped>
.secbackground {
  top: 3%;
  left: 2%;
  width: 96%;
  height: 100vh;
  position: fixed;
  z-index: 0;
  opacity: 90%;
  background-color: #f2f2f2;
}

.background {
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  position: fixed;
  z-index: -1;
  opacity: 30%;
}
</style>