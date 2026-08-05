import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from a .env file if present
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is missing. Please set it in your .env file or environment.")

client = OpenAI(api_key=api_key)

def get_text_embedding(text: str) -> list[float]:
    """Generates a 1536-dimension vector for an input string."""
    clean_text = text.replace("\n", " ")
    response = client.embeddings.create(
        input=[clean_text],
        model="text-embedding-3-small"
    )
    return response.data[0].embedding
