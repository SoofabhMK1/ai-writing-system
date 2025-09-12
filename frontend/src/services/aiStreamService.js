/**
 * Handles the streaming chat response from the AI API, which uses Server-Sent Events (SSE).
 *
 * @param {number} aiModelId - The ID of the AI model to use.
 * @param {Array<Object>} messages - The messages to send to the API.
 * @param {Object} callbacks - An object containing callback functions.
 * @param {Function} callbacks.onReasoning - Callback for 'reasoning' event chunks.
 * @param {Function} callbacks.onContent - Callback for 'content' event chunks.
 * @param {Function} callbacks.onError - Callback for 'error' events.
 */
export async function handleStreamedChat(
  aiModelId,
  messages,
  { onReasoning, onContent, onError },
) {
  try {
    const res = await fetch('/api/v1/ai/chat-stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ai_model_id: aiModelId,
        messages: messages,
      }),
    });

    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let currentEvent = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split('\n');
      buffer = lines.pop();

      for (const line of lines) {
        if (line.startsWith('event:')) {
          currentEvent = line.substring(6).trim();
        } else if (line.startsWith('data:')) {
          const dataStr = line.substring(5).trim();
          if (!dataStr) continue;

          try {
            const data = JSON.parse(dataStr);
            if (currentEvent === 'reasoning' && data.chunk) {
              onReasoning(data.chunk);
            } else if (currentEvent === 'content' && data.chunk) {
              onContent(data.chunk);
            } else if (currentEvent === 'error' && data.error) {
              onError(data.error);
            }
          } catch (e) {
            console.error('Failed to parse SSE data:', dataStr, e);
          }
        } else if (line.trim() === '') {
          currentEvent = '';
        }
      }
    }
  } catch (error) {
    console.error('Error during chat stream:', error);
    if (onError) {
      onError('An error occurred. Please try again.');
    }
  }
}
