# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
from langgraph.checkpoint.postgres import PostgresSaver

DB_URL = 'postgresql://postgres:999828gch@localhost:5432/postgres?sslmode=disable'

with PostgresSaver.from_conn_string(DB_URL) as checkpointer:
    # 获取所有的checkpoint
    checkpoints = checkpointer.list(
        {"configurable": {"thread_id": "1"}}
    )

    for checkpoint in checkpoints:
        messages = checkpoint[1]["channel_values"]["messages"]
        for message in messages:
            message.pretty_print()
        break
