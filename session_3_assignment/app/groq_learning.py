from groq import Groq
from phoenix.otel import register
from openinference.instrumentation.groq import GroqInstrumentor
from dotenv import load_dotenv

load_dotenv()

tracer_provider = register(
    project_name="financial-advisor",
    endpoint="http://localhost:6006/v1/traces"
)

GroqInstrumentor().instrument(
    tracer_provider=tracer_provider
)

client = Groq()

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Say hello in one sentence."
        }
    ],
    model="openai/gpt-oss-120b"
)

print(response.choices[0].message.content)