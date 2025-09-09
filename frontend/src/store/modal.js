// frontend/src/store/modal.js
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useModalStore = defineStore('modal', () => {
  const isOpen = ref(false);
  const title = ref('');
  const message = ref('');

  // 用于处理 Promise 的解析和拒绝
  let resolvePromise = null;
  let rejectPromise = null;

  // 打开模态框并返回一个 Promise
  const show = (newTitle, newMessage) => {
    title.value = newTitle;
    message.value = newMessage;
    isOpen.value = true;

    return new Promise((resolve, reject) => {
      resolvePromise = resolve;
      rejectPromise = reject;
    });
  };

  // 用户点击“确认”
  const confirm = () => {
    if (resolvePromise) {
      resolvePromise(true); // 解析 Promise，表示确认
    }
    isOpen.value = false;
  };

  // 用户点击“取消”或背景
  const cancel = () => {
    if (rejectPromise) {
      rejectPromise(false); // 拒绝 Promise，表示取消
    }
    isOpen.value = false;
  };

  return { isOpen, title, message, show, confirm, cancel };
});
