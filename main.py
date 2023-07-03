import openai
import os
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

function_descriptions = [
    {
        "name": "extract_info_from_email",
        "description": "Categorise & Extract key information from an email, such as use case, company name, contact details, and whether the email is a sales email or not.",
        "parameters": {
            "type": "object",
            "properties": {
                "companyName": {
                    "type": "string",
                    "description": "the name of the company that sent the email"
                },
                "useCase": {
                    "type": "string",
                    "description": "the purpose and the use case of this company's inquiry",
                },
                "priority": {
                    "type": "string",
                    "description": "Try to give a priority score to this email, based on how likely this email will lead to a good business opportunity for NFT business, from 1 to 10, with 1 being the lowest and 10 being the highest priority",
                },
                "category": {
                    "type": "string",
                    "description": " Try to categorise this email into categories like these, 1: customer support, 2: consulting, 3: job, 4: partnership, 5: sales, 6: others, 7: spam. If you can't categorise it, just leave it blank",
                },
                "nextStep": {
                    "type": "string",
                    "description": "Try to give a next step for this email",
                }
            },
            "required": ["companyName", "useCase", "contactDetails", "priority", "category", "nextStep"]
        }
    }
]


class Email(BaseModel):
    from_email: str
    content: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/")
def analyse_email(email: Email):
    content = email.content
    prompt = f"Please extract key information from this email: {content} "

    message = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=message,
        functions=function_descriptions,
        function_call="auto"
    )

    arguments = response.choices[0]["message"]["function_call"]["arguments"]
    companyName = eval(arguments).get("companyName")
    useCase = eval(arguments).get("useCase")
    priority = eval(arguments).get("priority")
    category = eval(arguments).get("category")
    nextStep = eval(arguments).get("nextStep")

    return {
        "companyName": companyName,
        "useCase": useCase,
        "priority": priority,
        "category": category,
        "nextStep": nextStep
    }
