# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()

agent = create_agent(
    model="deepseek:deepseek-chat"
)
# 手动建立：建立列表，把每轮的消息append到列表中，单一不能实现太多功能

results = agent.invoke({"messages": [{"role": "human", "content": "来一首宋词。"}]})

messages = results["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
    message.pretty_print()

messages_list = messages

message = {"role": "human", "content": "再来。"}
messages_list.append(message)

results = agent.invoke({"messages": messages_list})
messages = results["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
    message.pretty_print()
