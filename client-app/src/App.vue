<template>
  <main>
    <a-space direction="vertical" class="full-width" :size="[0, 48]">
      <a-layout>
        <a-layout-sider v-show="$route.meta.bar_show" class="sider">Sider</a-layout-sider>
        <a-layout>
          <a-layout-header v-show="$route.meta.header_show" class="header">Header</a-layout-header>
          <router-view/>
          <a-layout-footer v-show="$route.meta.footer_show" class="footer">Footer</a-layout-footer>
        </a-layout>
      </a-layout>
    </a-space>
  </main>
</template>

<script>
import Bar from "@/components/Bar.vue"

export default {
  components: {Bar}
}
</script>

<style scoped>
.full-width {
  width: 100%;
}

.header {
  text-align: center;
  color: #fff;
  height: 64px;
  padding-inline: 50px;
  line-height: 64px;
  background-color: #7dbcea;
}

.sider {
  text-align: center;
  line-height: 120px;
  color: #fff;
  background-color: #3ba0e9;
}

.footer {
  text-align: center;
  color: #fff;
  background-color: #7dbcea;
}
</style>

