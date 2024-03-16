import os
from humanloop import Humanloop

HUMANLOOP_API_KEY = "api_key_here"
OPENAI_KEY = "api_key_here"

humanloop = Humanloop(
    api_key=HUMANLOOP_API_KEY,
)


def response_return(messages):
    response = humanloop.chat_deployed(
        project="learn anything",
        inputs={
            "topic": "Anime",
            "para": "4"
        },
        messages=messages,
        provider_api_keys={
            "openai": OPENAI_KEY
        }
    )

    return response.data[0].output

messages = []
while True:
    inp = input("Enter a question")
    messages.append({"role":"user","content":inp})
    response = response_return(messages)
    messages.append({"role":"assistant","content":response})