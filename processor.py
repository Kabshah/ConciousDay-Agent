
import os
import requests
import streamlit as st
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()


def get_api_key():
    """Get API key from Streamlit secrets or environment variables"""
    # Try Streamlit secrets first (for deployment)
    if hasattr(st, 'secrets') and "OPENROUTER_API_KEY" in st.secrets:
        return st.secrets["OPENROUTER_API_KEY"]

    # Fallback to .env (for local development)
    return os.getenv("OPENROUTER_API_KEY")


PROMPT_TEMPLATE = """
You are a daily reflection and planning assistant. Your goal is to:
1. Reflect on the user's journal and dream input
2. Interpret the user's emotional and mental state
3. Understand their intention and 3 priorities
4. Generate a practical, energy-aligned strategy for their day

INPUT:
Morning Journal: {journal}
Intention: {intention}
Dream: {dream}
Top 3 Priorities: {priorities}

OUTPUT FORMAT:
1. Inner Reflection Summary
2. Dream Interpretation Summary
3. Energy/Mindset Insight
4. Suggested Day Strategy (time-aligned tasks)
"""


def process_input(journal, intention, dream, priorities):
    # Get API key
    api_key = get_api_key()

    if not api_key:
        st.error("API key not found. Please set OPENROUTER_API_KEY in your secrets or .env file.")
        return None

    # Format the prompt using LangChain's template
    prompt = PromptTemplate(
        input_variables=["journal", "intention", "dream", "priorities"],
        template=PROMPT_TEMPLATE
    ).format(
        journal=journal,
        intention=intention,
        dream=dream,
        priorities=priorities
    )

    # Make API call to OpenRouter
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:3000",  # Required by OpenRouter
                "X-Title": "ConsciousDay Agent"  # Your app name
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            },
            timeout=30  # Add timeout to prevent hanging
        )

        response.raise_for_status()  # Raises exception for 4XX/5XX errors
        return response.json()["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {str(e)}")
        return None
