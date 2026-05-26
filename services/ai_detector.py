import logging
from openai import AsyncOpenAI
from config import settings

logger = logging.getLogger(__name__)
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def analyze_text(text: str) -> dict:
    try:
        response = await client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert AI content detector for academic integrity. "
                        "Analyze the given text and return a JSON response with these exact keys:\n"
                        "- ai_probability: integer 0-100\n"
                        "- verdict: one of 'AI-Generated', 'Human-Written', 'Mixed'\n"
                        "- confidence: one of 'High', 'Medium', 'Low'\n"
                        "- analysis: list of 3 short bullet point strings explaining your findings\n"
                        "- recommendation: one sentence instructor recommendation\n"
                        "Return ONLY valid JSON, no extra text."
                    )
                },
                {"role": "user", "content": f"Analyze this text:\n\n{text[:4000]}"}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )
        import json
        result = json.loads(response.choices[0].message.content)
        return result
    except Exception as e:
        logger.error(f"OpenAI analysis failed: {e}")
        return {
            "ai_probability": 0,
            "verdict": "Error",
            "confidence": "Low",
            "analysis": ["Analysis failed due to an API error."],
            "recommendation": "Please try again."
        }
