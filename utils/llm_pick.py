from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()
def pick_llm(level: str):
    """
    Picks the appropriate LLM based on the provided level.

    Args:
        level (str): The level of the LLM to pick. Can be 'basic', 'intermediate', or 'advanced'.

    Returns:
        str: The name of the picked LLM.
    """
    if level.lower() == "basic":
        return ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0, max_output_tokens=1024)
    elif level.lower() == "intermediate":
        return ChatGoogleGenerativeAI(model="gemini-4.0", temperature=0, max_output_tokens=1024)
    elif level.lower() == "advanced":
        return ChatGoogleGenerativeAI(model="gemini-4.5", temperature=0, max_output_tokens=1024)
    else:
        raise ValueError("Invalid level provided. Choose from 'basic', 'intermediate', or 'advanced'.")