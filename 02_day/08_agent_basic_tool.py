# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()


# docstring 很重要
def get_weather(city: str) -> str:
    """
    # docstring for get_weather
    获取指定城市的天气
    :param city: str    :return: str
    """
    return f"{city}今天晴天。"


agent = create_agent(
    model="deepseek:deepseek-chat",
    tools=[get_weather]
)
'''
print(agent)  # <langgraph.graph.state.CompiledStateGraph object at 0x0000027DAA3AABD0>
print(agent.nodes)
# {
# '__start__': <langgraph.pregel._read.PregelNode object at 0x0000027DAA367C90>,
# 'model': <langgraph.pregel._read.PregelNode object at 0x0000027DAA367F10>,
# 'tools': <langgraph.pregel._read.PregelNode object at 0x0000027DAA3A2510>
# }
'''

# 调用工具
results = agent.invoke({"messages": [{"role": "human", "content": "上海今天的的天气怎么样？"}]})

messages = results["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
    message.pretty_print()

# 不调用工具（配置工具，但不乱用）
results = agent.invoke({"messages": [{"role": "human", "content": "上海常驻人口有多少？"}]})

messages = results["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
    message.pretty_print()
