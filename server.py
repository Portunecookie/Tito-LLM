import json
from fastapi import FastAPI, Body
from typing import List

from service.gen_versus_by_topic import gen_versus_by_topic
from service.gen_topic_by_words import gen_topic_by_words

app = FastAPI()


# /data/A POST 요청 핸들러
@app.post("/data/A")
async def post_concat_words(words: List[str] = Body(...)):
    topic = gen_topic_by_words(words)
    print(topic)
    # TODO: json 검증
    result = []
    for t in json.loads(topic):
        result.append(gen_versus_by_topic(t))

    return json.loads(result)


# /data/B POST 요청 핸들러
@app.post("/data/B")
async def echo_body(body: dict = Body(...)):
    return body


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
