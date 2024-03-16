import openai
import os
from traceloop.sdk import Traceloop
from traceloop.sdk.decorators import workflow, task, tool, agent
  
Traceloop.init(disable_batch=True, api_key="XXXXXXX")

openai.api_key=os.environ["OPENAI_API_KEY"]
os.environ["SERPER_API_KEY"] = "XXXXXXXX" # serper.dev API key

# You can choose to use a local model through Ollama for example. See https://docs.crewai.com/how-to/LLM-Connections/ for more information.

# os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
os.environ["OPENAI_MODEL_NAME"] ='gpt-3.5-turbo'  # Adjust based on available model
# os.environ["OPENAI_API_KEY"] ='sk-111111111111111111111111111111111111111111111111'

#client = openai.api_client(api_key=os.environ["OPENAI_API_KEY"])

@task(name="joke_creation")
def create_joke():
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Tell me a joke on animals. Your joke tokens should strictly range between 25-15 tokens."}],
    )

    return completion.choices[0].message.content

@task(name="signature_generation")
def generate_signature(joke: str):
    completion = openai.Completion.create(
        model="davinci-002",
        prompt="add a signature to the joke:\n\n" + joke,
    )

    return completion.choices[0].text

@agent(name="joke_translation")
def translate_joke_to_pirate(joke: str):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Translate the below joke to cowboy-like english:\n\n{joke}"}],
    )

    history_jokes_tool()

    return completion.choices[0].message.content


@tool(name="history_jokes")
def history_jokes_tool():
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"get some history jokes"}],
    )

    return completion.choices[0].message.content


@workflow(name="pirate_joke_generator")
def joke_workflow():
    eng_joke = create_joke()
    pirate_joke = translate_joke_to_pirate(eng_joke)
    signature = generate_signature(pirate_joke)
    print(pirate_joke + "\n\n" + signature)

while True:
    value = input("Enter an input")
    joke_workflow()
