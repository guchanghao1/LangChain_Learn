# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
from langchain.agents import create_agent
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

# langchain的记忆管理方法：InMemorySave
checkpointer = InMemorySaver()

agent = create_agent(
    model="deepseek:deepseek-chat",
    checkpointer=checkpointer,
)
config = {"configurable": {"thread_id": "1"}}
# 第一轮
results = agent.invoke(
    {"messages": [{"role": "human", "content": "来一首宋词。"}]},
    config=config,
)

messages = results["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
    message.pretty_print()

# 第二轮
results = agent.invoke(
    {"messages": [{"role": "human", "content": "再来。"}]},
    config=config,
)

messages = results["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
    message.pretty_print()
