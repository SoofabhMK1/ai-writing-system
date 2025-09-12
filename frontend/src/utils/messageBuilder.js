/**
 * Prepares the message list for sending to the AI API.
 * It handles adding the system prefix if one is selected.
 *
 * @param {Array<Object>} messages - The current list of message objects.
 * @param {string|null} systemPrefix - The system prefix content to prepend.
 * @returns {Array<Object>} The final list of messages ready for the API.
 */
export function prepareMessagesForApi(messages, systemPrefix) {
  const messagesToSend = [...messages];
  if (systemPrefix) {
    messagesToSend.unshift({ role: 'system', content: systemPrefix });
  }
  
  // Filter out the 'thinking' part from assistant messages
  return messagesToSend.map(msg => {
    if (msg.role === 'assistant') {
      return { role: 'assistant', content: msg.content };
    }
    return { role: msg.role, content: msg.content };
  });
}
