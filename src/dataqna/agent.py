import os
import aisuite as ai
from openai import OpenAI
from dotenv import load_dotenv
from . import tools
_ = load_dotenv()


client = ai.Client()

def get_completions_from_messages(
        model: str, 
        messages: str, 
        temperature: float=1.0
) -> str:

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": f"{messages}"}
        ],
        temperature=temperature,
        tools=[tools.schema_extract],
        max_turns=5
    )

    return response.choices[0].message.content


def generate_code(
        model: str,
        schema: str,
        question: str
) -> str:
    prompt = f"""
        You are a data analyst. Given the schema and the user's question, write a python code for analysis.
        df and pd already exist. Do not read any file. Use print() to output results.
        If client ask you generate a chart, charts should be saved into path: Path(".") / "src" / "dataqna" / "output" / "chart_name.png"
        Schema:
        {schema}

        User's question:
        {question}

        Respond with the python code only.

    """

    response = get_completions_from_messages(model, prompt)

    return response


def generate_response(
        model: str,
        schema: str,
        code: str,
        result: str,
        question: str
) -> str:
    prompt = f"""
        You are a data analyst. Given the schema, the user's question, code, result from code, generate a analysis for client.

        Schema:
        {schema}

        User's question:
        {question}

        Code:
        {code}

        Result:
        {result}
    """

    response = get_completions_from_messages(model, prompt)

    return response

