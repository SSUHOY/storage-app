<template>
  <main>
    <header>
      <router-view/>
      <nav>
        <router-link to="/">Главная</router-link>
        <router-link to="/categories">Папки</router-link>
        <router-link to="/create">Создание папки</router-link>
      </nav>
    </header>

  </main>

</template>

<style scoped>
header {
  line-height: 1.5;
  display: flex;
  flex-direction: column;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
