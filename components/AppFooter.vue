<script>
export default {
  computed: {
    currentYear() {
      const today = new Date()
      return today.getFullYear()
    }
  }
}
</script>

<template>
  <footer class="footer">
    <p class="text-center">
      © Akkireddy {{ currentYear }}. Made with
      <a href="https://www.nuxtjs.org">NuxtJS</a> and
      <a href="https://ntl.fyi/3jJX1My">Netlify</a> 💚.
    </p>
  </footer>
</template>

<style lang="scss">
@import '../styles/_settings.scss';

.footer {
  text-align: center;
  border-top: 2px solid $c-border;
}
</style>
