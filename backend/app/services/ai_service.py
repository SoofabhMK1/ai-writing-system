# backend/app/services/ai_service.py
from openai import AsyncOpenAI
from app.core.security import decrypt_data
from app.models.setting import AIModel
from app.services.prompt_service import create_outline_generation_prompt

from typing import AsyncGenerator

async def generate_outline_from_config(
    model_config: AIModel,
    prompt: str,
) -> AsyncGenerator[str, None]:
    """
    Generates a novel outline as a stream based on the provided prompt.
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
            content = chunk.choices[0].delta.content or ""
            yield content
            
    except Exception as e:
        # In a real app, you'd want more robust error handling here.
        # For now, we'll just yield an error message.
        yield f"Error: {str(e)}"
