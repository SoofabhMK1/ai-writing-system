<!-- src/components/NavBar.vue -->
<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="navbar-logo">AI Writer</div>
      <div class="navbar-menu">
        <router-link to="/" class="navbar-link">项目</router-link>
        <router-link to="/conversation" class="navbar-link">对话</router-link>
        <router-link to="/characters" class="navbar-link">角色库</router-link>
        <router-link to="/settings" class="navbar-link">设定集</router-link>
      </div>
    </div>
  </nav>
</template>

<script setup></script>

<style scoped>
.navbar {
  background-color: var(--color-surface);
  height: 64px; /* Consistent height */
  display: flex;
  justify-content: center;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 1000;
  border-bottom: var(--border-width) solid var(--color-border);
  box-shadow: var(--shadow-sm);
  padding: 0 var(--spacing-8);
  transition: background-color var(--transition-base);
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.navbar-logo {
  color: var(--color-text);
  cursor: default; /* Change cursor to default as it's not clickable */
  text-decoration: none;
  font-size: var(--font-size-xl);
  font-weight: 600;
  display: flex;
  align-items: center;
  transition: color var(--transition-base);
}

.navbar-logo:hover {
  /* No hover effect for a non-clickable element */
  color: var(--color-text);
}

.navbar-menu {
  display: flex;
  align-items: center;
  gap: var(--spacing-4);
}

.navbar-link {
  color: var(--color-text-muted);
  text-decoration: none;
  padding: var(--spacing-2) var(--spacing-3);
  font-size: var(--font-size-base);
  font-weight: 500;
  border-radius: var(--border-radius-md);
  transition: var(--transition-base);
}

.navbar-link:hover {
  color: var(--color-text);
  background-color: var(
    --color-surface-hover,
    rgba(255, 255, 255, 0.05)
  ); /* Fallback for hover */
}

.navbar-link.router-link-exact-active {
  color: var(--color-primary);
  font-weight: 600;
}
</style>
