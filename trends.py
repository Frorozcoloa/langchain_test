from googlesearch import search
from newspaper import Article
import json
import os
from dotenv import load_dotenv
import pandas as pd
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

template = """
Input: Given the following news about a sports e-commerce, conduct an analysis of potential future trends
return a list of 1-3 topics.
Output is a JSON list with the following format
[
    {{"topic_name": "<topic1>", "topic_description": "<topic_description1>", "product_to_sell": "<product_to_sell1>"}},}}, 
    {{"topic_name": "<topic2>", "topic_description": "<topic_description2>", "product_to_sell": "<product_to_sell2>"}},}},
    ...
]
{news}
"""
prompt = PromptTemplate(template=template, input_variables=["news"])

llm = ChatOpenAI(
    openai_api_key=os.getenv("CODEGPT_API_KEY"),
    openai_api_base=os.getenv("CODEGPT_API_BASE"), 
    model=os.getenv("CODEGPT_AGENT_ID"))

llm_chain = LLMChain(prompt=prompt, llm=llm)

def get_articles_trends(query : str =  "Sports market trends", num_results: int = 10):
    list_text = []
    for url in search(query,num_results=num_results):
        article = Article(url)
        article.download()
        article.parse()
        list_text.append(article.text)
    return list_text

def get_analysis_trends(list_text : list):
    values_to_return = []
    for text in list_text:
        try:
            topics_raw = llm_chain.run(text)
            topics_dict = json.loads(topics_raw.replace("```","").replace("json", ""))
            values_to_return += topics_dict
        except:
            continue
    return values_to_return

def main():
    list_text = get_articles_trends()
    analysis = get_analysis_trends(list_text)
    df = pd.DataFrame.from_dict(analysis)
    print(df.head())
    df.to_csv("trends.csv")

if __name__ == "__main__":
    main()