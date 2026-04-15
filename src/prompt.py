from langchain_core.prompts import ChatPromptTemplate

def build_prompt():
    SYSTEM_PROMPT = """
    You are a helpful Amazon shopping assistant.
    Answer the question using ONLY the following context (real product reviews + metadata).
    Always cite the product ASIN when possible."""

    return ChatPromptTemplate.from_template(
    f"""{SYSTEM_PROMPT}

        context:
        {{context}}

        question: 
        {{question}}

        Answer based on the Amazon datasets:
    """
    )