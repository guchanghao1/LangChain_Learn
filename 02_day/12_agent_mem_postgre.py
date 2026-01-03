# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
# pip install psycopg langgraph-checkpoint-postgres

from langgraph.checkpoint.postgres import PostgresSaver
from langchain.agents import create_agent
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

DB_URL = "postgresql://postgres:999828gch@localhost:5432/postgres"
with PostgresSaver.from_conn_string(DB_URL) as checkpointer:
    # checkpointer.setup()# 创建数据库，只运行一次
    agent = create_agent(
        model="deepseek:deepseek-chat",
        checkpointer=checkpointer,
    )
    config = {"configurable": {"thread_id": "1"}}
    # 第三轮
    results = agent.invoke(
        {"messages": [{"role": "human", "content": "来一首相同作者的宋词。"}]},
        config=config,
    )

    messages = results["messages"]
    print(f"历史消息：{len(messages)}条")
    for message in messages:
        message.pretty_print()
