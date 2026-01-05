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

# 第一种 message-message
for event in agent.stream(
        {"messages": [{"role": "human", "content": "上海今天的的天气怎么样？"}]},
        stream_mode="values"  # 以消息为单位
):
    messages = event["messages"]
    print(f"历史消息：{len(messages)}条")
    # for message in messages:
    #     message.pretty_print()
    messages[-1].pretty_print()

# 第二种（这是两个主要的，还要多种） token-token
'''
for chunk in agent.stream(
        {"messages": [{"role": "human", "content": "上海今天的的天气怎么样？"}]},
        stream_mode="messages"  # 以token为单位
):
    print(chunk[0].content, end="")
    # print(chunk)
    # (AIMessageChunk
    # (
    # content='晴天',
    # additional_kwargs={},
    # response_metadata={'model_provider': 'deepseek'},
    # id='lc_run--019b7c4e-18ca-7aa0-9b8a-de3550018a3f'
    # ),
    # {'langgraph_step': 3,
    # 'langgraph_node': 'model',
    # 'langgraph_triggers': ('branch:to:model',),
    # 'langgraph_path': ('__pregel_pull', 'model'),
    # 'langgraph_checkpoint_ns': 'model:e5899c7a-ec16-5526-139d-f1add7ba81fb',
    # 'checkpoint_ns': 'model:e5899c7a-ec16-5526-139d-f1add7ba81fb',
    # 'ls_provider': 'deepseek',
    # 'ls_model_name': 'deepseek-chat',
    # 'ls_model_type': 'chat',
    # 'ls_temperature': None}
    # )
'''
