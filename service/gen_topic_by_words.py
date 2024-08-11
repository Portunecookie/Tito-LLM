import json
from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import FewShotChatMessagePromptTemplate
from langchain_teddynote.messages import stream_response
import os
from dotenv import load_dotenv

load_dotenv()


def gen_topic_by_words(topic: str):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

    # TODO: 벡터 유사도로 example 고르기.
    examples = [
        {
            "input": '["연애","자취","비밀번호"]',
            "output": '["연애하는 사이에서, 연인에게 자취방 비밀번호를 알려줘도 되는가?","연애하는 사이에서 금전적 비용을 정확하게 따져야 하는가?","자취 생활 중에 연인을 자주 초대하는 것이 좋은가?","연인이 자취 중인 경우 동거처럼 되는 상황이 괜찮은가?","자취를 하면 연애가 더 쉬워지는가?"]',
        },
    ]
    example_prompt = ChatPromptTemplate.from_messages(
        [("human", "{input}"), ("ai", "{output}")]
    )

    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt, examples=examples
    )

    final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an AI bot that generates 5 debate topics that can be divided into an A vs B format, following the given example format, and outputs them in a JSON array format.",
            ),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )

    result = llm.invoke(final_prompt.format_messages(input=topic)).content
    print(f"Generated Topic : {result}")

    try:
        return json.loads(result)
    except:
        raise Exception("Failed to convert JSON")
