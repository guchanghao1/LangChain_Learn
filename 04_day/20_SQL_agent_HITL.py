# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
import requests, pathlib
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

# 下载简单的数据库
url = "https://storage.googleapis.com/benchmarks-artifacts/chinook/Chinook.db"
local_path = pathlib.Path("Chinook.db")

if local_path.exists():
    print(f"{local_path}已存在。")
else:
    response = requests.get(url)
    if response.status_code == 200:
        local_path.write_bytes(response.content)
        print(f"{local_path}下载成功")
    else:
        print(f"下载失败，状态码：{response.status_code}")
# 初始化模型
load_dotenv()

model = init_chat_model(
    model="deepseek:deepseek-chat",
    temperature=0.5
)
# 访问数据库
db = SQLDatabase.from_uri("sqlite:///Chinook.db")

print(f"Dialect:{db.dialect}")
"""“方言”（dialect）指的是不同数据库系统（如PostgresSQL、MySQL、SQLite等）之间的差异。
这些差异包括SQL语法、数据类型、事务处理、连接方式等。每个数据库系统都有自己独特的特性，
就像不同地区的人说不同的方言一样。"""
print(f"Available tables:{db.get_usable_table_names()}")
print(f'Sample output: {db.run("SELECT * FROM Artist LIMIT 5;")}')
# 使用工具包
toolkit = SQLDatabaseToolkit(db=db, llm=model)
tools = toolkit.get_tools()
for tool in tools:
    print(f"{tool.name}: {tool.description}")
# 构建智能体
system_prompt = """
你是一个与数据库交互的智能体。
给定输入问题，创建语法正确的{dialect}来运行。
查看查询结果并返回答案，若是用户给定了输出结果的个数，最后输出结果就是{top_k}个。
""".format(
    dialect=db.dialect,
    top_k=3,
)

# 加入human-in-the-loop中断机制

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt,
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={"sql_db_query": True},
            description_prefix="Tool execution requires approval",
        ),
    ],
    checkpointer=InMemorySaver(),
)

question = "哪钟曲目的平均时间最长？"
config = {"configurable": {"thread_id": "sql_agent"}}

for step in agent.stream(
        {"messages": [{"role": "human", "content": question}]},
        stream_mode="values",
        config=config,
):
    step["messages"][-1].pretty_print()

# HITL的决策判断
if "__interrupt__" in step:
    print("INTERRUPTED")
    interrupt = step["__interrupt__"][0]
    for request in interrupt.value["action_requests"]:
        print(request["description"])
elif "messages" in step:
    step["messages"][-1].pretty_print()
else:
    pass

# human进行决策
for step in agent.stream(
        Command(resume={"decisions": [{"type": "approve"}]}),
        config=config,
        stream_mode="values",
):
    if "messages" in step:
        step["messages"][-1].pretty_print()
    if "__interrupt__" in step:
        print("INTERRUPTION")
        interrupt = step["__interrupt__"][0]
        for request in interrupt.values["action_requests"]:
            print(request["description"])
    else:
        pass
