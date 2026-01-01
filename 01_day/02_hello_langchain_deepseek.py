# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
"""（旧版）
from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv

load_dotenv()

model = ChatDeepSeek(
    model="deepseek-chat",# deepseek-reasoner
    temperature=0.3,
    max_tokens=2000,
    timeout=None,
    max_retries=2
)

for chunk in model.stream("来一段毛泽东的诗词。"):
    print(chunk.content,end="",flush=True)
"""
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv()


model = init_chat_model(
    model="deepseek-chat",  # model="deepseek:deepseek-chat",
    model_provider="deepseek",  # 可省略
    temperature=1,
)
for chunk in model.stream("来一段毛泽东的诗词。"):
    print(chunk.content, end="", flush=True)  # 同上
