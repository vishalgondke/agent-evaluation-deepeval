from deepeval.models import AnthropicModel
import os
from dotenv import load_dotenv

load_dotenv()

eval_model = AnthropicModel(
    model="claude-sonnet-5-5",
    api_key=os.getenv("ANTHROPIC_API_KEY")
)