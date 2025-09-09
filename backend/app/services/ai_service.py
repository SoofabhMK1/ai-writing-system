# backend/app/services/ai_service.py
from openai import AsyncOpenAI
from app.core.security import decrypt_data
from app.models.setting import AIModel

async def generate_outline_from_config(
    model_config: AIModel,
    core_concept: str,
    worldview: dict | None,
    writing_style: dict | None,
    target_word_count: int
) -> dict:
    """
    Generates a novel outline based on the provided configuration.
    """
    # 1. Decrypt the API key
    decrypted_api_key = decrypt_data(model_config.api_key)

    # 2. Construct the prompt
    prompt = f"""
You are a world-class novelist and story architect. Your task is to generate a detailed, chapter-by-chapter outline for a new novel.

**Core Concept (Seed):**
{core_concept}

**Target Word Count:** Approximately {target_word_count} words.

**Worldview / Genre:**
Name: {worldview.get('name', 'Not specified')}
Description: {worldview.get('description', 'Not specified')}
Genre: {worldview.get('genre', 'Not specified')}
Additional Details: {worldview.get('additional_details', 'None')}

**Writing Style:**
Name: {writing_style.get('name', 'Not specified')}
Tone: {writing_style.get('tone', 'Not specified')}
Point of View: {writing_style.get('point_of_view', 'Not specified')}
Guidelines: {writing_style.get('guidelines', 'None')}

Based on all the information above, please generate a complete novel outline. The outline should be structured chapter by chapter. For each chapter, provide a title and a concise summary of the key events, character developments, and plot points.

Please provide the output in a structured JSON format. The root object should have a single key "chapters", which is an array of chapter objects. Each chapter object should have two keys: "title" and "summary".

Example format:
{{
  "chapters": [
    {{
      "title": "Chapter 1: The Unexpected Inheritance",
      "summary": "Our protagonist, a down-on-their-luck librarian, discovers they have inherited a mysterious, ancient bookstore from a relative they never knew."
    }},
    {{
      "title": "Chapter 2: The Hidden Library",
      "summary": "While exploring the bookstore, the protagonist finds a hidden door leading to a secret library filled with magical, sentient books."
    }}
  ]
}}
"""

    # 3. Initialize the client and make the API call
    client = AsyncOpenAI(
        base_url=model_config.api_url,
        api_key=decrypted_api_key,
    )

    response = await client.chat.completions.create(
        model=model_config.model_name,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )

    # 4. Parse and return the result
    try:
        outline_json = response.choices[0].message.content
        return {"status": "success", "outline": outline_json}
    except Exception as e:
        return {"status": "error", "message": f"Failed to parse AI response: {str(e)}"}
