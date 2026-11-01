def pick_llm(level: str):
    """
    Picks the appropriate LLM based on the provided level.

    Args:
        level (str): The level of the LLM to pick. Can be 'basic', 'intermediate', or 'advanced'.

    Returns:
        str: The name of the picked LLM.
    """
    if level.lower() == "basic":
        return "gemini-3.8-flash"
    elif level.lower() == "intermediate":
        return "gemini-4.0"
    elif level.lower() == "advanced":
        return "gemini-4.5"
    else:
        raise ValueError("Invalid level provided. Choose from 'basic', 'intermediate', or 'advanced'.")