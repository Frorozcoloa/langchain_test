from dotenv import load_dotenv
import os

load_dotenv()

codegpt_api_key = os.getenv("CODEGPT_API_KEY")
code_gpt_agent_id = os.getenv("CODEGPT_AGENT_ID")

# Set API base URL
codegpt_api_base = os.getenv("CODEGPT_API_BASE")
openai_api_key = os.getenv("OPENAI_API_KEY")
