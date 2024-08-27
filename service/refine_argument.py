import json
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import FewShotChatMessagePromptTemplate
import os
from dotenv import load_dotenv
from typing import List
from langchain.schema.messages import HumanMessage, SystemMessage

load_dotenv()


def refine_argument(content: str):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)
    s = SystemMessage(
        content='You are an AI bot that listens to a discussion between two people and edits the content to make it more suitable for a smooth debate. You also supplement any lacking evidence and correct any inappropriate language or terms for a formal discussion setting. Finally, you provide explanations for the changes made. Please output in JSON format. {"content_edited": "", "reason":[]}'
    )
    h = HumanMessage(content=content)

    result = llm.invoke([s,h]).content
    print(f"Generated THINGS: {result}")

    try:
        return json.loads(result)
    except:
        return result


refine_argument(
    """
저는 지방에서 사는 것이 수도권에서 사는 것보다 이점이 있다고 생각합니다.
우선, 말씀하신 자녀 교육 측면에서 사교육은 지방에서 하는 것이 존나 이점이 있다고 생각합니다. 우선, 예를 들어 대구의 수성구 같은 곳은 수도권의 사교육만큼 발달되어있습니다. 그리고 사교육비 같은 경우도 절대 만만하지 않기 때문에 지방에서 사교육을 받는 것이 더 이점이 있다고 생각합니다.
또한, 서울에서의 교통은 대중교통은 의미가 있을지 몰라도, 자가용을 사용해야 하는 경우에는 오히려 교통 인프라에서 이점을 얻지 못한다고 생각합니다. 
그러니까 내 말이 맞는거야 이 빵꾸똥꾸야."""
)
