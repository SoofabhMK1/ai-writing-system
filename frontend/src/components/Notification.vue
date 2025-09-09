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
  top: 20px;
  right: 20px;
  z-index: 2000;
  width: 320px;
}

.notification {
  background-color: #fff;
  color: #fff;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  font-weight: 500;
  text-align: center;
}

.notification-success {
  background-color: #4CAF50;
}

.notification-error {
  background-color: #e94b3c;
}

.notification-info {
  background-color: #4a90e2;
}

.notification-fade-enter-active,
.notification-fade-leave-active {
  transition: all 0.5s ease;
}

.notification-fade-enter-from,
.notification-fade-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>
