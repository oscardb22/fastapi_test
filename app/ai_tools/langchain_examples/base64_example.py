import base64

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings

llm = ChatGoogleGenerativeAI(
    model="models/gemini-3.1-flash-lite-preview",
    api_key=settings.GOOGLE_API_KEY,
    temperature=0.9,
)
byte_image = base64.b64encode(open("example.jpg", "rb").read()).decode("utf-8")
message = HumanMessage(
    content=[
        {"type": "text", "text": "What is the plate"},
        {"type": "image_url", "image_url": f"data:image/jpeg;base64,{byte_image}"}
    ]
)
response = llm.invoke([message])
print(response.content)
