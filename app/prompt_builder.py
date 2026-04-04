from app.prompts import PROMPT_TEMPLATE


def build_prompt(user_text: str) -> str:
    """Build prompt from template.
    Args:
        user_text (str): User input text."""
    prompt_text = PROMPT_TEMPLATE.format(user_text=user_text)
    return prompt_text


prompt = build_prompt(user_text='Hello')
