from langchain_core.prompts import ChatPromptTemplate

def build_prompt():
    """
    Return prompt to be given to the LLM.

    Parameters
    ----------
    None

    Returns
    -------
    string
        LLM prompt with placeholders for context and question.
    """

    SYSTEM_PROMPT = """
    You are a helpful Amazon shopping assistant.
    Answer the question using ONLY the following context (real product reviews + metadata).
    Always cite the product ASIN when possible.
    Also cite the specific content that supports your response."""

    return ChatPromptTemplate.from_template(
    f"""{SYSTEM_PROMPT}

        context:
        {{context}}

        question: 
        {{question}}

        Answer based on the Amazon datasets:
    """
    )