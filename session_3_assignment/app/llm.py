import os

from groq import Groq
from dotenv import load_dotenv
from phoenix.otel import register
from openinference.instrumentation.groq import GroqInstrumentor

load_dotenv()

phoenix_endpoint = os.getenv("PHOENIX_ENDPOINT")

tracer_provider = register(
    project_name="financial-advisor",
    endpoint=phoenix_endpoint
)

GroqInstrumentor().instrument(
    tracer_provider=tracer_provider
)

def build_system_prompt(context):
    client_portfolio = context["client_portfolio"]
    policy = context["policy"]
    news = context["news"]

    prompt = f"""
You are an assistant for Apex Financial Partners.

CLIENT PORTFOLIO
{client_portfolio}

RISK POLICY
{policy}

CURRENT STOCK NEWS
{news}
"""

    return prompt

def get_llm_response(context, user_query):
    system_prompt = build_system_prompt(context)

    client = Groq()

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_query
            }
        ],
        model="openai/gpt-oss-120b"
    )

    return response.choices[0].message.content

# if __name__ == "__main__":
#     context = {
#         "client_portfolio": {
#             "client": {
#                 "client_id": 1042,
#                 "risk_tolerance": "Conservative"
#             }
#         },
#         "policy": {
#             "page": 109,
#             "text": "Conservative clients have allocation limits."
#         },
#         "news": [
#             {
#                 "title": "Example TSLA headline"
#             }
#         ]
#     }

#     print(build_system_prompt(context))

# if __name__ == "__main__":
    from app.services.context_service import get_context

    context = get_context(1042, "TSLA")

    user_query = (
        "I want to buy $15,000 worth of TSLA stock today. "
        "Given my current portfolio and your internal risk policies, "
        "is this allowed? Also, is there any bad news about TSLA today?"
    )

    answer = get_llm_response(context, user_query)

    print(answer)