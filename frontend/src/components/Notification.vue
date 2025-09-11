<!-- frontend/src/components/Notification.vue -->
<template>
  <div class="notification-container">
    <transition-group name="notification-fade" tag="div">
      <div 
        v-for="notification in notifications.items" 
        :key="notification.id" 
        :class="['notification', `notification-${notification.type}`]"
      >
        {{ notification.message }}
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { useNotificationStore } from '@/store/notification.js';
const notifications = useNotificationStore();
</script>

<style scoped>
.notification-container {
  position: fixed;
  top: var(--spacing-8);
  right: var(--spacing-8);
  z-index: 2000;
  width: 350px;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-4);
}

.notification {
  color: #ffffff;
  padding: var(--spacing-4) var(--spacing-5);
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-lg);
  font-weight: 500;
  font-size: var(--font-size-base);
  text-align: left;
  border: var(--border-width) solid transparent;
}

.notification-success {
  background-color: var(--color-success);
  border-color: var(--color-success);
}

.notification-error {
  background-color: var(--color-danger);
  border-color: var(--color-danger);
}

.notification-info {
  background-color: var(--color-primary);
  border-color: var(--color-primary);
}

.notification-fade-enter-active,
.notification-fade-leave-active {
  transition: all 0.3s ease-in-out;
}

.notification-fade-enter-from,
.notification-fade-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
