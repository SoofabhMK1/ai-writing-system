import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useModalStore = defineStore('modal', () => {
  // State for the original ConfirmationModal
  const isOpen = ref(false);
  const title = ref('');
  const message = ref('');
  let resolvePromise = null;
  let rejectPromise = null;

  // State for the new PreviewSendModal
  const isPreviewOpen = ref(false);
  const previewContent = ref('');
  let previewResolve = null;
  let previewReject = null;

  // --- Methods for ConfirmationModal ---

  const show = (newTitle, newMessage) => {
    title.value = newTitle;
    message.value = newMessage;
    isOpen.value = true;

    return new Promise((resolve, reject) => {
      resolvePromise = resolve;
      rejectPromise = reject;
    });
  };

  const confirm = () => {
    if (resolvePromise) {
      resolvePromise(true);
    }
    isOpen.value = false;
    resetConfirmationState();
  };

  const cancel = () => {
    if (rejectPromise) {
      const error = new Error('Operation canceled by user.');
      error.isCanceled = true;
      rejectPromise(error);
    }
    isOpen.value = false;
    resetConfirmationState();
  };

  function resetConfirmationState() {
    resolvePromise = null;
    rejectPromise = null;
  }

  // --- Methods for PreviewSendModal ---

  const showPreview = (content) => {
    previewContent.value = content;
    isPreviewOpen.value = true;

    return new Promise((resolve, reject) => {
      previewResolve = resolve;
      previewReject = reject;
    });
  };

  const confirmPreview = () => {
    if (previewResolve) {
      previewResolve(true);
    }
    isPreviewOpen.value = false;
    resetPreviewState();
  };

  const cancelPreview = () => {
    if (previewReject) {
      const error = new Error('Sending canceled by user.');
      error.isCanceled = true;
      previewReject(error);
    }
    isPreviewOpen.value = false;
    resetPreviewState();
  };

  function resetPreviewState() {
    previewContent.value = '';
    previewResolve = null;
    previewReject = null;
  }

  return { 
    // For ConfirmationModal
    isOpen, 
    title, 
    message, 
    show, 
    confirm, 
    cancel,

    // For PreviewSendModal
    isPreviewOpen,
    previewContent,
    showPreview,
    confirmPreview,
    cancelPreview,
  };
});
