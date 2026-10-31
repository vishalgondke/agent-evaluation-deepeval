from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
model = init_chat_model(model="claude-opus-5")

# response = model.invoke("Tell me about the history of the Eiffel Tower.")

# print(response.content)