# Import necessary libraries
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import os
import json

from langchain.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

# Load environment variables from .env file
load_dotenv()

template = "You are a helpful assistant. Your task is to analyze the users of an ecommerce."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = """
    Please, identify the main topics mentioned in these comments. 

    Return a list of 3 topics. 
    Output is a JSON list with the following format
    [
        {{"topic_name": "<topic1>", "topic_description": "<topic_description1>"}}, 
        {{"topic_name": "<topic2>", "topic_description": "<topic_description2>"}},
        ...
    ]
    Customer reviews:
    {customer_reviews}
"""
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

# Retrieve API key and agent ID from environment variables
codegpt_api_key= os.getenv("CODEGPT_API_KEY")
code_gpt_agent_id= os.getenv("CODEGPT_AGENT_ID")

# Set API base URL
codegpt_api_base = "https://api.codegpt.co/v1"

# Create a ChatOpenAI object with the retrieved API key, API base URL, and agent ID
llm = ChatOpenAI(openai_api_key=codegpt_api_key,
                openai_api_base=codegpt_api_base,
                model=code_gpt_agent_id)

# Create a list of messages to send to the ChatOpenAI object
chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)
messages = chat_prompt.format_prompt(
    customer_reviews ="I love biking, hiking and walking. I like to get to know new towns, talk to people. I hate when plans don't happen, I'm very strict with times. I love to eat, I always like to go to good restaurants and try the food, I don't like to see many dishes and I hate the noise, I like the countryside and live there."
)

# Send the messages to the ChatOpenAI object and retrieve the response
response = llm(messages.to_messages())

# Print the response
print(json.loads(response.content.replace("```","").replace("json", "")))