import ast
import os
import re

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

MODEL = "gpt-4o-mini"

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


REGEX = re.compile(r"^(?P<start>```)?(?(start)python\n|)(?P<code>.*)\n(?P=start)$", re.DOTALL)

def remove_codetags(text: str) -> str:
    return REGEX.sub(r"\g<code>", text)


def ask_number_code(question: str, answer: str | float | int, additional_info: str = "") -> str:
    extra_info = f"Additional context: {additional_info}" if additional_info else ""
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""I am creating a number-input question. The question is: "{question}"

                {extra_info}

                The correct answer is "{answer}".
                Write me the python code to solve the question. Use variables when possible.
                Answer with only the python code. Do not use the input and print functions.""",
            }
        ],
        model=MODEL,
    )
    for choice in chat_completion.choices:
        if content := choice.message.content:
            print(remove_codetags(content))
    res = chat_completion.choices[0].message.content
    # check that res is a list of strings
    assert isinstance(res, str)
    return remove_codetags(text=res)


def ask_mc_options(
    options: list[str], answer: str, question: str, num_to_generate: int
) -> list[str]:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""I am creating a multiple choice question. The question is: "{question}"
                Here are the options: {options}. The correct answer is "{answer}". Generate me {num_to_generate} incorrect options.
                Answer with only a python list of strings.""",
            }
        ],
        model=MODEL,
    )
    for choice in chat_completion.choices:
        if content := choice.message.content:
            print(remove_codetags(content))
    content = chat_completion.choices[0].message.content
    try:
        res = ast.literal_eval(remove_codetags(content)) if content else []
    except Exception as e:
        print(e)
        res = content.split("\n") if content else []
    # check that res is a list of strings
    assert isinstance(res, list)
    assert all(isinstance(x, str) for x in res)
    return res

