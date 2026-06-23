import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


def get_openai_client():
    """
    Creates OpenAI client if API key exists.
    Returns None if key is missing.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return None

    return OpenAI(api_key=api_key)


def call_llm(prompt, model="gpt-4.1-mini"):
    """
    Calls OpenAI model and returns text.
    Falls back gracefully if key or API call fails.
    """

    client = get_openai_client()

    if client is None:
        return None

    try:
        response = client.responses.create(
            model=model,
            input=prompt
        )

        return response.output_text

    except Exception as error:
        print(f"LLM call failed: {error}")
        return None