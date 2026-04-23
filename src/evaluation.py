from rag_pipeline import get_retrievers, lcel_pipeline, get_llm_prompt, build_context
from ragas import EvaluationDataset, evaluate
from langchain_groq import ChatGroq
from ragas.metrics import Faithfulness, FactualCorrectness
from ragas.llms import LangchainLLMWrapper

def build_dataset(queries, references):
    """
    Build dataset for RAG evaluation purpose, by including retrieved contexts (based on documents),
    RAG response, given query, and given references.

    Parameters
    ----------
    queries : list of str
        a list of user queries.
    refereneces : list of str
        a list of "ground truth" responses to compare RAG response to.

    Returns
    -------
    list
        A list of dict, including user query, retrieved contexts (for generation),
        LLM response, and reference to compare to.
    """
    dataset = []
    print("Building Dataset...")
    for query, reference in zip(queries, references):
        llm, prompt_template = get_llm_prompt("llama-3.1-8b-instant")
        _, _, hybrid_retriever = get_retrievers(5)
        docs = hybrid_retriever.invoke(query)
        retrieved_contexts = build_context(docs).split("\n\n---\n\n")
        response = lcel_pipeline(query, hybrid_retriever, llm, prompt_template)
        dataset.append(
            {
                "user_input":query,
                "retrieved_contexts":retrieved_contexts,
                "response":response,
                "reference":reference
            }
        )
    return dataset

if __name__ == '__main__':
    # Follow this tutorial: https://docs.ragas.io/en/stable/getstarted/rag_eval/
    sample_queries = [
        "something comfortable for floor stretching",
        "something that stinks"
    ]

    # Generated based on Gemini with the same prompt
    gemini_answers = [
        """
        Based on the provided context, here are the most comfortable options for floor stretching:
        * Day 1 Fitness Folding Gymnastics Gym Mat (ASIN: B07DQ8XXFW): This is described as an "extremely comfortable floor pad for working out and stretching" and features high-density foam that provides cushioning without being too soft.
        * Ultimate Body Press Exercise and Yoga Mat (ASIN: B07LBN1Y5T): This 2-inch thick four-panel folding mat is highly recommended for those with hard floors. A reviewer noted they are "glad I did" get it to "stretch and practice flexibility inside where I only have hard floors."
        * Gaiam Yoga Mat (ASIN: B07W62HK9M): This 5mm thick mat is noted for its ability to make hard surfaces comfortable. One reviewer mentioned it provides "enough padding to be comfortable when sitting or stretching" even on a "concrete floor."
        * Harbinger Recyclable Foam Eco Fit Exercise Mat (ASIN: B00NIGVNI6): While this 3/8-inch mat is described as "very comfortable for sure," be aware that the review mentions it is "very stretchy" and "has no grip on the floor," which caused the user to slip during exercises like downward dog.
        """,
        """
        Based on the provided reviews, several products are noted specifically for having strong or unpleasant odors:
        * Simply Kids Knee and Elbow Pads (ASIN: B07CN291K3): A reviewer reported a "horrible smell" described as "chemicals they use at a car wash" or an "artificial cherry scent" that persisted even after airing out for weeks.
        * Barrington Billiards Dartboard Cabinet Set (ASIN: B07FP1LXPJ): One customer stated it "smells like pure gasoline" and another noted the entire room smelled like "Sex Panther cologne" due to styrofoam melting during transit.
        * Power Systems Rubber Octagonal Dumbbell (ASIN: B00660E50Y): A user described a "repulsive odor" that feels "unhealthy" to breathe while working out and has been difficult to clean off.
        * CAMTOA Tactical Vest (ASIN: B00ZXKRCPI): This product reportedly "stinks like fuel" or "gas o lean," leading the reviewer to wonder if it is a water repellent or a fire hazard.
        * Los Angeles Dodgers Air Freshener (ASIN: B005D3L1S4): Ironically, this air freshener is described as having "nothing pleasant about the odor" and smelling "like Windex."
        * GZNIGHT Bicycle Handlebar Bag (ASIN: B079GZGJ7Z): A very brief one-star review simply states, "It stinks."
        * J2 Sport NCAA T-Shirt (ASIN: B06XG1TG28): The reviewer noted that while the quality is good, it "stinks a little im the wash and dry."
        * If you are looking to fix a "stink" rather than buy one, the Chimera Fight Exchange Refillable Boxing Glove Deodorizers (ASIN: B08W6TVWHG) are specifically designed to eliminate bad odors from gym bags and sports gear.
        """
    ]
    
    evaluation_dataset = EvaluationDataset.from_list(build_dataset(sample_queries, gemini_answers))
    evaluator_llm = LangchainLLMWrapper(ChatGroq(model="llama-3.3-70b-versatile"))
    # Asked GPT: How to use `from ragas.metrics.collections import ContextRecall` with `evaluate`?
    results = evaluate(
        dataset=evaluation_dataset,
        metrics=[Faithfulness(), FactualCorrectness()],
        llm=evaluator_llm
    )
    print('\n Result:')
    print(results)