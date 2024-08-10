from langchain_community.chat_models import ChatOllama
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.prompts import FewShotChatMessagePromptTemplate
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()


def gen_versus_by_topic(input_words: List[str]):
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

    examples = [
        {
            "input": '"자취를 하면 연애가 더 쉬워지는가?"',
            "output": '{"A": "쉬워진다", "B": "어려워진다"}',
        },
    ]
    # 요약을 위한 프롬프트 템플릿 정의
    example_prompt = ChatPromptTemplate.from_messages(
        [("human", "{input}"), ("ai", "{output}")]
    )

    # few shot prompt
    few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt, examples=examples
    )

    # 최종 prompt
    final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an AI bot that generates arguments for both sides, A and B, based on the given debate topic and outputs them in JSON format.",
            ),
            few_shot_prompt,
            ("human", "{input}"),
        ]
    )

    # stream_response(llm.stream(final_prompt.format_messages(input=input_words)))
    result = llm.invoke(final_prompt.format_messages(input=input_words)).content
    print(result)
    return result
