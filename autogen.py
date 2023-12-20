from autogen import (
    AssistantAgent,
    UserProxyAgent,
    config_list_from_json,
    GroupChat,
    GroupChatManager,
)

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

llm_config = {
    "config_list": config_list,
    "seed": 53,
    "temperature": 0,
}

user_proxy = UserProxyAgent(
    name="Admin",
    system_message="A human administrator. Interacts with the Data scientist to discuss trend findings. The conclusions of the trends must be approved by this admin.",
    code_execution_config=False,
    llm_config=llm_config,
)

engineer = AssistantAgent(
    name="Engineer",
    llm_config=llm_config,
    system_message="""Engineer. You assist the Data scientist, writing python/shell code to solve tasks. You wrap the 
    code in a code block that specifies the type of script. The user cannot modify your code. So don't suggest 
    incomplete code that requires others to modify it. Don't use a code block if it is not intended to be executed by 
    the executor. Don't include multiple code blocks in the same response. Do not ask others to copy and paste the result. 
    Check the execution result returned by the executor. If the result indicates that there is an error, correct the error and 
    reissue the code. Suggest full code rather than partial code or code changes. If the error cannot be fixed 
    or if the task is not solved even after the code is executed correctly, analyze the problem, review your 
    your assumption, gather the additional information you need, and think of a different approach to test.""",
)

planner = AssistantAgent(
    name="Data scientist",
    system_message="""Data Scientist. Propose a data analysis, to see the trend of the e-commerce market. Draw the conclusions of the analysis based on the comments of the administrators and reviewers.  An engineer who knows how to write code and an administrator and reviewer who does not write code can participate in the analysis. 
    Explain the idea you have for the analysis and make it clear what step an engineer, an Executorand a Critic performs. Talk to the summary to summaries the text an get information and the reviewer, so you can have more context.""",
    llm_config=llm_config,
)
reviewer = AssistantAgent(
    name="reviewer",
    system_message="""
    reviewer: You are the test user and everyone wants to ask you questions about how to buy in an e-commerce, your job is to give product ideas for the e-commerce of a sportswear company, give your ideas to the administrator and data scientist so he can deliver a good analysis of the market trend.
    """,
    llm_config=llm_config,
)
executor = AssistantAgent(
    name="Executor",
    system_message="Executor. Execute the code written by the engineer and report the result.And if they don't know how to start you tell the engineer to make a code to get searches related to e-commerce in google or duckduckgo, maybe the first 5 pages.",
    code_execution_config={"last_n_messages": 3, "work_dir": "feedback"},
    llm_config=llm_config,
)

critic = AssistantAgent(
    name="Critic",
    system_message="Critic. Check the analysis, claims and code of other agents and send your comments.",
    llm_config=llm_config,
)
analist = AssistantAgent(
    name="Summary",
    system_message="Your job is to read all the documents, give a summary, or part of them. You must communicate to the data scientist the information you found in order to organize it.",
    llm_config=llm_config,
)


groupchat = GroupChat(
    agents=[user_proxy, engineer, planner, executor, critic, analist, reviewer],
    messages=[],
    max_round=50,
)
manager = GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager,
    message="""
                         They must deliver a file with detailed analysis of the energy clothing e-commerce market trends, they must deliver a .csv with the information of the name of the trending products and why. The idea is to increase sales and recommend the products that are trending. Start by extracting information in intener, it can be google searches or start here the file C:/Users/EQUIPO/Desktop/personal/codegpt/tendencias.txt that have a news for fitness tend.
                         """,
)
