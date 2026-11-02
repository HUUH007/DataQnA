import os
import aisuite as ai
from openai import OpenAI
from dotenv import load_dotenv
_ = load_dotenv()


client = ai.Client()

def get_completions_from_messages(
        model: str, 
        messages: str, 
        temperature: float=1.0
) ->str:

    responce = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": f"{messages}"}
        ],
        temperature=temperature
    )

    return responce.choice[0].message.content


