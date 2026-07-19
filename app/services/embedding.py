import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_text_embedding(text: str) -> list[float]:
    """Generates a 1536-dimension vector for an input string."""
    clean_text = text.replace("\n", " ")
    response = client.embeddings.create(
        input=[clean_text],
        model="text-embedding-3-small"
    )
    return response.data[0].embedding
