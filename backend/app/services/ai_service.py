# backend/app/services/ai_service.py
from openai import AsyncOpenAI
from app.core.security import decrypt_data
from app.models.setting import AIModel
from app.services.prompt_service import create_outline_generation_prompt

from typing import AsyncGenerator

import json

async def generate_outline_from_config(
    model_config: AIModel,
    prompt: str,
) -> AsyncGenerator[str, None]:
    """
    Generates a novel outline as a stream based on the provided prompt.
    This function is designed to handle models that support separate 'reasoning_content'
    and 'content' fields in the stream, such as deepseek-reasoner.
    It yields Server-Sent Events (SSE) formatted strings.
    """
    # 1. Decrypt the API key
    decrypted_api_key = decrypt_data(model_config.api_key)

    # 2. Initialize the client
    client = AsyncOpenAI(
        base_url=model_config.api_url,
        api_key=decrypted_api_key,
    )

    # 3. Make the streaming API call
    try:
        stream = await client.chat.completions.create(
            model=model_config.model_name,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )
        async for chunk in stream:
            delta = chunk.choices[0].delta
            
            # Check for reasoning_content (for models like deepseek-reasoner)
            reasoning_chunk = getattr(delta, 'reasoning_content', None)
            if reasoning_chunk:
                # SSE format: event name and data
                data = json.dumps({"chunk": reasoning_chunk})
                yield f"event: reasoning\ndata: {data}\n\n"

            # Check for the final content
            if delta.content:
                data = json.dumps({"chunk": delta.content})
                yield f"event: content\ndata: {data}\n\n"

    except Exception as e:
        # In a real app, you'd want more robust error handling here.
        # For now, we'll just yield an error message as a custom event.
        data = json.dumps({"error": str(e)})
        yield f"event: error\ndata: {data}\n\n"
