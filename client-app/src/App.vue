<template>
  <main>
    <Bar v-show="$route.meta.bar_show"/>
    <router-view/>
  </main>
</template>

<script>
  import Bar from "@/components/Bar.vue"
  export default {
    components: {Bar}
  }
</script>

<style>
header {
  line-height: 1.5;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }
}
</style>
