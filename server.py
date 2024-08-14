import json
from fastapi import FastAPI, Body
from typing import List

from service.gen_versus_by_topic import gen_versus_by_topic
from service.gen_topic_by_words import gen_topic_by_words

app = FastAPI()


@app.post("/generate-topic")
async def post_concat_words(words: List[str] = Body(...)):
    topic_list = gen_topic_by_words(words)
    versus_list = []
    for topic in topic_list:
        versus_result = gen_versus_by_topic(topic)
        obj_to_add = {}
        obj_to_add["topic"] = topic
        obj_to_add["A"] = versus_result["A"]
        obj_to_add["B"] = versus_result["B"]

        versus_list.append(obj_to_add)

    return versus_list


@app.post("/data/B")
async def echo_body(body: dict = Body(...)):
    return body


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
