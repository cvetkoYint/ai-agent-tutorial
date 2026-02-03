import os
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from zai import ZaiClient
from langchain.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_agent
from langgraph.prebuilt import create_react_agent
from pydantic import SecretStr

load_dotenv()
zai_api_key = SecretStr(os.getenv("ZAI_API_KEY", ""))


class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]


# Used for connecting with
llm = ChatOpenAI(
    model="glm-4.7",
    api_key=zai_api_key,
    base_url="https://api.z.ai/api/coding/paas/v4",
)

system_prompt = "You are a research assistant that will help generate a research paper. Answer the user query and use neccessary tools. Wrap the output in this format and provide no other text"

# This should be an instruction for a model how to return message.
# but it doesn't want to work. Investigate/Ask colleagues.
promptTemplate = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

agent = create_agent(
    model=llm,
    system_prompt=system_prompt,
    response_format=ResearchResponse,
    tools=[],
)

response = agent.invoke(
    {"messages": [{"role": "human", "content": "Who's bakaprase?"}]}
)

print("Response starting here:", response["structured_response"])
