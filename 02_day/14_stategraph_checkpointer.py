# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
# checkpointer:检查点管理器，表现形式：存储
# checkpoint：检查点，状态图的总体状态快照（某一时刻或步骤）
# thread_id进行管理
# 作用：记忆管理、时间旅行（time travel）、pause(human-in-the-loop)、容错（退回步骤，重新走）

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver  # checkpointer
from langchain_core.runnables import RunnableConfig
from typing import Annotated
from typing_extensions import TypedDict
from operator import add


# 表达状态:整个状态图的状态
class State(TypedDict):
    foo: str
    bar: Annotated[list[str], add]

# 节点
def node_a(state: State):
    return {"foo": "a", "bar": ["a"]}


def node_b(state: State):
    return {"foo": "b", "bar": ["b"]}


# 构建状态图
workflow = StateGraph(State)
workflow.add_node(node_a)
workflow.add_node(node_b)
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

# 检查点管理器
checkpointer = InMemorySaver()

# 运行工作流
graph = workflow.compile(checkpointer=checkpointer)

# 配置
config: RunnableConfig = {
    "configurable": {"thread_id": "1"}
}

# 调用
results = graph.invoke({"foo": ""}, config=config)
# print(results)
# {'foo': 'b', 'bar': ['a', 'b']}  add
# {'foo': 'b', 'bar': ['b']}  无add

# 状态查看
# print(graph.get_state(config=config))
# StateSnapshot(
# values={'foo': 'b', 'bar': ['a', 'b']},
# next=(),
# config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f0e7d29-989a-6033-8002-2f86e6b329b3'}},
# metadata={'source': 'loop', 'step': 2, 'parents': {}},
# created_at='2026-01-02T12:00:15.356728+00:00',
# parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f0e7d29-9897-691d-8001-bfff11b5a885'}},
# tasks=(),
# interrupts=()
# )


# 深入扩展
for checkpoint_tuple in checkpointer.list(config=config):
    # print()
    # print(checkpoint_tuple)
    # CheckpointTuple(
    # config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f0e7d2e-e0f4-6325-8002-a36744efe41e'}},
    # checkpoint={
    # 'v': 4,
    # 'ts': '2026-01-02T12:02:37.161142+00:00',
    # 'id': '1f0e7d2e-e0f4-6325-8002-a36744efe41e',
    # 'channel_versions': {
    # '__start__': '00000000000000000000000000000002.0.11498963658718231',
    # 'foo': '00000000000000000000000000000004.0.7067769753798947',
    # 'branch:to:node_a': '00000000000000000000000000000003.0.8793597380221404',
    # 'bar': '00000000000000000000000000000004.0.7067769753798947',
    # 'branch:to:node_b': '00000000000000000000000000000004.0.7067769753798947'
    # },
    # 'versions_seen': {
    # '__input__': {},
    # '__start__': {'__start__': '00000000000000000000000000000001.0.7029900457839496'},
    # 'node_a': {'branch:to:node_a': '00000000000000000000000000000002.0.11498963658718231'},
    # 'node_b': {'branch:to:node_b': '00000000000000000000000000000003.0.8793597380221404'}},
    # 'updated_channels': ['bar', 'foo'],
    # 'channel_values': {'foo': 'b', 'bar': ['a', 'b']}
    # },
    # metadata={
    # 'source': 'loop',
    # 'step': 2,
    # 'parents': {}
    # },
    # parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1f0e7d2e-e0f1-6c1c-8001-8459e9cccae0'}},
    # pending_writes=[]
    # )
    print()
    print(checkpoint_tuple[2]['step'])
    print(checkpoint_tuple[2]['source'])
    print(checkpoint_tuple[1]['channel_values'])
"""

2
loop
{'foo': 'b', 'bar': ['a', 'b']}

1
loop
{'foo': 'a', 'bar': ['a'], 'branch:to:node_b': None}

0
loop
{'foo': '', 'branch:to:node_a': None}

-1
input
{'__start__': {'foo': ''}}
"""
