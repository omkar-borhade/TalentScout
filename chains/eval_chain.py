# Uses same structure as question_chain, but for evaluation
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

def get_eval_chain(api_key, model_name):
    if not api_key: return None
    llm = ChatGroq(groq_api_key=api_key, model_name=model_name, temperature=0.2, streaming=True)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an interviewer evaluator. ONLY return valid JSON, no explanations."),
        ("user", "{question}")
    ])
    return prompt | llm | StrOutputParser()
