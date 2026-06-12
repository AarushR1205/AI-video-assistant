from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
import os

def get_llm():
    return ChatMistralAI(model="mistral-large-latest", mistral_api_key=os.getenv("MISTRAL_API_KEY"), temperature=0.2)

def build_chain(system_prompt: str):
    llm = get_llm()
    return (RunnablePassthrough() | RunnableLambda(lambda x: {"text": x}) |
            ChatPromptTemplate.from_messages([("system", system_prompt), ("human", "{text}")]) | 
            llm | StrOutputParser())

def extract_action_items(transcript: str)->str:
    system_prompt = """You are an expert meeting analyst. From the meeting transcript
                    extract all the action items. For each provide:
                    - Task description
                    - Ownerk (who is responsible)
                    - Deadline (if mentioned, else write 'Not specified')
                    Format as a numbered lisst. If none found say 'No actions found'"""
    chain = build_chain(system_prompt)
    return chain.invoke(transcript[:2500])

def extract_key_decisions(transcript: str) -> str:
    chain = build_chain("""You are an expert meeting analyst. From the meeting transcript, "
        extract all key decisions made. Format as a numbered list. "
        If none found say 'No key decisions found.""")
    return chain.invoke(transcript[:2500])


def extract_questions(transcript: str) -> str:
    chain = build_chain("""From the meeting transcript, extract all unresolved questions "
        or topics needing follow-up. Format as a numbered list.
        If none found say 'No open questions found.""")
    return chain.invoke(transcript[:2500])