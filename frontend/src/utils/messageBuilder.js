import { useConversationStore } from '@/store/conversation';
import { usePromptPresetStore } from '@/store/promptPreset';

/**
 * Filters out the 'thinking' part from assistant messages.
 * @param {Array} messages - The array of message objects.
 * @returns {Array} A new array of messages with 'thinking' parts removed.
 */
function filterThinking(messages) {
  return messages.map(({ role, content }) => ({ role, content }));
}

/**
 * Formats the conversation history into a string for the prompt.
 * @param {Array} messages - The array of historical message objects.
 * @returns {string} A formatted string representing the conversation history.
 */
function formatHistory(messages) {
  if (!messages || messages.length === 0) {
    return 'No history yet.';
  }
  return messages
    .map(msg => {
      const role = msg.role.charAt(0).toUpperCase() + msg.role.slice(1);
      return `[${role}]: ${msg.content}`;
    })
    .join('\n');
}

/**
 * Builds the final array of messages to be sent to the AI API,
 * based on the selected preset and conversation history.
 *
 * @param {Array} allMessages - The complete list of messages in the current conversation.
 * @returns {Array} The structured message array for the API.
 */
export function prepareMessagesForApi(allMessages) {
  const conversationStore = useConversationStore();
  const presetStore = usePromptPresetStore();

  const { selectedPresetId } = conversationStore;
  const selectedPreset = presetStore.presets.find(p => p.id === selectedPresetId);

  // The last message is the new user input.
  const currentUserInput = allMessages[allMessages.length - 1]?.content || '';
  // All messages before the last one are history.
  const historyMessages = allMessages.slice(0, -1);

  const cleanHistory = filterThinking(historyMessages);
  const formattedHistory = formatHistory(cleanHistory);

  const finalMessages = [];

  if (selectedPreset) {
    // Using a preset
    if (selectedPreset.system_prompt) {
      finalMessages.push({ role: 'system', content: selectedPreset.system_prompt });
    }
    if (selectedPreset.cot_guidance) {
      finalMessages.push({ role: 'system', content: selectedPreset.cot_guidance });
    }

    const userMessageContent =
      `<history>\n${formattedHistory}\n</history>\n\n` +
      `<user_input>\n${currentUserInput}\n</user_input>`;
    finalMessages.push({ role: 'user', content: userMessageContent });

    if (selectedPreset.other_instructions) {
      finalMessages.push({ role: 'system', content: selectedPreset.other_instructions });
    }
  } else {
    // No preset selected, fall back to a simple history + user input format
    const cleanMessages = filterThinking(allMessages);
    finalMessages.push(...cleanMessages);
  }

  return finalMessages;
}
