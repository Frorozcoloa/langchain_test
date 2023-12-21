import autogen
config_list = autogen.config_list_from_json(env_or_file="OAI_CONFIG_LIST.json")

llm_config = {
    "config_list": config_list,
    "seed": 53,
    "temperature": 0,
}


    
user_proxy = autogen.UserProxyAgent(
   name="Admin",
   system_message="A human admin. Interact with the Data Analyst to discuss the user description. The new user description needs to be approved by this Admin",
   code_execution_config=False,
)

data_analyst = autogen.AssistantAgent(
    name="Data Analyst",
    system_message="""
        Data Analyst. you read a text and asks the Reviewer
        about the question and.
        You must delete the user description and create a new one, give for example: the user is a person have the next problem and recommender to uses this elements.
        You talk that Critic that confirm the new hypothesis and change the user description
        """,
    code_execution_config=False,
    llm_config=llm_config,
)

engineer = autogen.AssistantAgent(
    name = "Engineer",
    system_message = "Engineer. you must create a code in python to save the new user description in the <id_user>.txt",
    llm_config=llm_config,
)


executor = autogen.AssistantAgent(
    name="Executor",
    system_message="Executor. execute the code wirte by Engineer",
    code_execution_config={"last_n_messages": 3, "work_dir": "feedback"},
    llm_config=llm_config,
)

reviwer = autogen.AssistantAgent(
    name="Reviewer",
    system_message="Reviewer. your role involves simulating user behaviora and interacting with the Data Analyst",
    llm_config=llm_config,
)

critic = autogen.AssistantAgent(
    name="Critic",
    system_message="Critic. Your job is to analyze the user's new description and accept it as long as they have changed their profile and it is clear which products they are interested in. You say to engennier that save the new user description in the <id_user>.txt",
    llm_config=llm_config,
)
groupchat = autogen.GroupChat(
    agents=[user_proxy, engineer, data_analyst, executor, reviwer],
    messages=[],
    max_round=50,
)
user_review = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    user_review,
    message="""There is a user with ID 1234451 who enjoys mountain biking. Cycling clothing, glasses, and other gear have been recommended to them, but they have not made any purchases. We have noticed an increase in their searches for therapeutic items, such as orthopedic collars and small weights, among others. We have also observed a change in location from a mountainous area with few inhabitants to a larger area.""",
)
