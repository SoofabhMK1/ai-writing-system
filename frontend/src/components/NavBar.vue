<!-- src/components/NavBar.vue -->
<template>
  <nav class="navbar">
    <div class="navbar-container">
      <router-link to="/" class="navbar-logo">
        AI Writer
      </router-link>
      <div class="navbar-menu">
        <router-link to="/characters" class="navbar-link">角色库</router-link>
        <router-link to="/settings" class="navbar-link">设定集</router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
</script>

<style scoped>
.navbar {
  background-color: #ffffff;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 1.2rem;
  position: sticky;
  top: 0;
  z-index: 999;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  height: 60px;
  z-index: 1;
  width: 100%;
  max-width: 1100px;
  padding: 0 24px;
}

.navbar-logo {
  color: #2c3e50;
  justify-self: flex-start;
  cursor: pointer;
  text-decoration: none;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  font-weight: bold;
}

.navbar-menu {
  display: flex;
  align-items: center;
}

.navbar-link {
  color: #2c3e50;
  text-decoration: none;
  padding: 0 1rem;
  font-size: 1rem;
  font-weight: 500;
  transition: color 0.3s;
}

.navbar-link:hover {
  color: #4a90e2;
}
</style>
