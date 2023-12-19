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

template = "You are a helpful assistant. Your task is to analyze the products of an ecommerce."
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = """
    Please, identify the main topics mentioned in these comments. 

    Return a list of 10-20 topics. 
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
codegpt_api_base = os.getenv("CODEGPT_API_BASE")

# Create a ChatOpenAI object with the retrieved API key, API base URL, and agent ID
llm = ChatOpenAI(openai_api_key=codegpt_api_key,
                openai_api_base=codegpt_api_base,
                model=code_gpt_agent_id)

# Create a list of messages to send to the ChatOpenAI object
chat_prompt = ChatPromptTemplate.from_messages(
    [system_message_prompt, human_message_prompt]
)
messages = chat_prompt.format_prompt(
    customer_reviews ="""
Small 10-liter hiking backpack nh100 quechua black, BENEFITS
Carrying comfort, COMFORT CARRYING COMFORT Spalder and padded straps 
1 main compartment with double zipper 
VOLUME
Volume: 10 liters | Weight: 145 g | Dimensions: 39 x 21 x 12 cm.friction resistance
FRICTION RESISTANCE
Durable, abrasion-resistant materials and joints. 10-year warranty. Warranty 10 years.Ventilation
VENTILATION
Simple to use backrest
EASE OF USE
Easy access to the external pocket by placing the backpack in a horizontal position while hiking.
"""
)

# Send the messages to the ChatOpenAI object and retrieve the response
response = llm(messages.to_messages())

# Print the response
print(json.loads(response.content.replace("```","").replace("json", "")))