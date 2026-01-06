# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
from langchain.agents import create_agent
from dotenv import load_dotenv
from tavily import TavilyClient
from typing import Literal
from langchain.tools import tool
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model(
    model="deepseek:deepseek-chat",
    temperature=0.7,
)

tavily_client = TavilyClient()


@tool
def inferent_search(
        query: str,
        max_results: int = 4,
        topic: Literal["general", "news", "finance"] = "general",
        include_raw_content: bool = False,
):
    """网站搜索工具"""
    return tavily_client.search(
        query=query,
        max_results=max_results,
        topic=topic,
        include_raw_content=include_raw_content,
    )


system_prompt = """你是一个专业的研究员，你的任务是进行系统地研究并生成一份完整的研究报告。
可以使用的工具如下：
inferent_search：用于搜索互联网信息
请注意：
1.全面收集信息
2.验证信息的准确性
3.组织总结信息，编写结构化的研究报告
4.总结报告内容的时效性"""

agent = create_agent(
    model=model,
    system_prompt=system_prompt,
    tools=[inferent_search],
)

query = "什么是AI应用开发，详细介绍岗位情况、岗位特点、岗位要求技能、岗位职责。"

for envent in agent.stream(
        {"messages": [{"role": "human", "content": query}]},
        stream_mode="values",
):
    envent["messages"][-1].pretty_print()
