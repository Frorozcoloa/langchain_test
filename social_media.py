from openai import OpenAI
import base64
from pathlib import Path
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.docstore.document import Document

from config import openai_api_key

model = OpenAI(api_key=openai_api_key)

def image_b64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def look(image_path, prompt="Describe this image"):
    b64_image = image_b64(image_path)

    response = model.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{b64_image}",
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    }
                ]
            }
        ],
        max_tokens=1024,
    )

    message = response.choices[0].message
    return message.content

def read_all_images():
    images_paths = Path("images").iterdir()
    description = {}
    for image_path in images_paths:
        if image_path.is_dir():
            read_images = image_path.glob("*.jpg")
            for image in read_images:
                describe = look(image)
                doc = Document(page_content=describe, metadata={"source": image_path.name})
                if description.get(image_path.name) is None:
                    description[image_path.name] = [doc]
                
                else:
                    description[image_path.name].append(doc)
    return description


def get_template():
    template = "You are a helpful assistant. Your task is to analyze to draw common topic from the given descriptions"
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = """
        Please, identify the main topics mentioned in these images. 

        Return a list of 3-5 topics. 
        Output is a JSON list with the following format
        [
            {{"topic_name": "<topic1>", "topic_description": "<topic_description1>"}}, 
            {{"topic_name": "<topic2>", "topic_description": "<topic_description2>"}},
            ...
        ]
        Images:
        {images}
    """
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )
    return chat_prompt

