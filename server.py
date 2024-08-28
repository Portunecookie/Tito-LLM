import json
import time
from fastapi import FastAPI, Body, requests
from typing import List

from service.gen_versus_by_topic import gen_versus_by_topic
from service.gen_topic_by_words import gen_topic_by_words
from service.refine_argument import refine_argument

app = FastAPI()


@app.post("/generate-topic")
async def post_concat_words(words: List[str] = Body(...)):
    print(words)
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


@app.post("/refine-argument")
async def post_refine_argument(argument: str = Body(...)):
    data = refine_argument(argument)

    return data


@app.get("/health-check")
async def echo_body(body: dict = Body(...)):
    return "OK"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8977)

    # Kuma Health Check
    print("Starting Kuma Health Check")
    while True:
        try:
            requests.get(
                "https://kuma.owsla.duckdns.org/api/push/R9DEJUpsyt?status=up&msg=OK"
            )
        except Exception as e:
            print(f"Request failed: {e}")
        time.sleep(60)
