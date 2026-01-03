# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
# 人在回路 human in the loop
# agent 集成大模型 集成工具 调用工具 中断机制
# 人的确认 ：approve reject edit
# 中间件 middleware

"""
更复杂的智能体 create_agent
大模型：model
系统提示词：system_prompt
工具：工具运行时上下文传递参数：content_schema
记忆管理：checkpointer
结构化输出：response_format
"""

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

from langchain.tools import tool, ToolRuntime  # 运行时上下文

from langchain.agents.structured_output import ToolStrategy

from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.types import Command

from dataclasses import dataclass  # 数据类,用于传参数
from dotenv import load_dotenv

load_dotenv()

# Define system prompt
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question 

that they mean wherever they are, use the get_user_location tool to find their location.
用中文回答。"""

# Define context schema
@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str


# Define tools
@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"


# Configure model
model = init_chat_model(
    model="deepseek:deepseek-chat",
    temperature=0.5
)


# Define response format
@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    # A punny response (always required)
    punny_response: str
    # Any interesting information about the weather if available
    weather_conditions: str | None = None


# Set up memory
checkpointer = InMemorySaver()

# Create agent
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "get_user_location": True,
                "get_weather_for_location": {
                    "allowed_decisions": ["approve", "reject"]
                },
            },
            description_prefix="工具执行挂起等待决策"
        )
    ],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)

# Run agent
# `thread_id` is a unique identifier for a given conversation.
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather outside?"}]},
    config=config,
    context=Context(user_id="1")
)

messages = response["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
    message.pretty_print()

if "__interrupt__" in response:
    print("INTERRUPTED")
    interrupt = response["__interrupt__"][0]
    for request in interrupt.value["action_requests"]:
        print(request["description"])

response = agent.invoke(
    Command(
        resume={"decisions": [{"type": "approve"}]}
    ),
    config=config,
    context=Context(user_id="1")
)

messages = response["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
    message.pretty_print()

if "__interrupt__" in response:
    print("INTERRUPTED")
    interrupt = response["__interrupt__"][0]
    for request in interrupt.value["action_requests"]:
        print(request["description"])

response = agent.invoke(
    Command(
        resume={"decisions": [{"type": "approve"}]}
    ),
    config=config,
    context=Context(user_id="1")
)

messages = response["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
    message.pretty_print()
