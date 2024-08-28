import json
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import FewShotChatMessagePromptTemplate
import os
from dotenv import load_dotenv
from typing import List
from langchain.schema.messages import HumanMessage, SystemMessage
from langchain_community.callbacks import get_openai_callback


load_dotenv()


def refine_argument(content: str):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    s = SystemMessage(
        content="""You are an AI bot that listens to a discussion between two people and edits the content to make it more suitable for a smooth debate.
        You also supplement any lacking evidence and correct any inappropriate language or terms for a formal discussion setting.
        Finally, you provide explanations in Korean for the changes made.
        Please respond in the following JSON format : {"content_edited": "string", "explanation": ["string"]}""",
    )
    h = HumanMessage(content=content)

    with get_openai_callback() as cb:
        result = llm.invoke([s, h]).content
        print(cb)

    print(f"Generated THINGS: {result}")

    try:
        return json.loads(result)
    except:
        return result
