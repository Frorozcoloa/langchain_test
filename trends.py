from googlesearch import search
from newspaper import Article
import json
import os
from dotenv import load_dotenv
import pandas as pd
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document

load_dotenv()

template = """
Given the following docs about a sports e-commerce, conduct an analysis of potential future trends.
return a list of 25-50 topics.
Output is a JSON list with the following format
[
    {{"product_decription": "<product_decription>", "product_to_sell": "<product_to_sell1>"}},}}, 
    {{"product_decription": "<product_decription>", "product_to_sell": "<product_to_sell2>"}},}},
    ...
]
{docs}
"""
template_summary = """
        The following is a set of documents:

        {docs}

        Based on this list of docs, please identify the main themes 

        Helpful Answer:
"""
prompt_summary = PromptTemplate(template=template_summary, input_variables=["news"])
prompt_topic = PromptTemplate(template=template, input_variables=["news"])
llm = ChatOpenAI(
    openai_api_key=os.getenv("CODEGPT_API_KEY"),
    openai_api_base=os.getenv("CODEGPT_API_BASE"), 
    model=os.getenv("CODEGPT_AGENT_ID"))

llm_summary = LLMChain(prompt=prompt_summary, llm=llm)
llm_topic = LLMChain(prompt=prompt_topic, llm=llm)

def get_articles_trends(query : str =  "Sports market trends", num_results: int = 50):
    list_text = []
    for url in search(query,num_results=num_results):
        article = Article(url)
        article.download()
        article.parse()
        doc = Document(page_content=article.text,  metadata={"source": url})
        list_text.append(doc)
    return list_text

def get_analysis_trends(list_docs : list):
    combine_documents_chain = StuffDocumentsChain(
        llm_chain=llm_summary, document_variable_name="docs"
    )
    reduce_documents_chain = ReduceDocumentsChain(
        # This is final chain that is called.
        combine_documents_chain=combine_documents_chain,
        # If documents exceed context for `StuffDocumentsChain`
        collapse_documents_chain=combine_documents_chain,
        # The maximum number of tokens to group documents into.
        token_max=4000,
    )
    map_reduce_chain = MapReduceDocumentsChain(
        # Map chain
        llm_chain=llm_summary,
        # Reduce chain
        reduce_documents_chain=reduce_documents_chain,
        # The variable name in the llm_chain to put the documents in
        document_variable_name="docs",
        # Return the results of the map steps in the output
        return_intermediate_steps=False,
    )
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    split_docs = text_splitter.split_documents(list_docs)
    text_summary = map_reduce_chain.run(split_docs)
    raw_topics = llm_topic.run(text_summary)
    topics_raw = json.loads(raw_topics.replace("```","").replace("json", ""))
    return topics_raw

def main():
    list_text = get_articles_trends()
    analysis = get_analysis_trends(list_text)
    df = pd.DataFrame.from_dict(analysis)
    print(df.head())
    df.to_csv("trends.csv")

if __name__ == "__main__":
    main()