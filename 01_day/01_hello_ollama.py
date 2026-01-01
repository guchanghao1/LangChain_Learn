# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
'''# 旧版
from langchain_ollama import ChatOllama

model = ChatOllama(
    model='deepseek-r1:7b',
    base_url='http://localhost:11434/',  # ???
    temperature=0.2
)
for chunk in model.stream('给我一篇现代诗词'):
    print(chunk.content, end='', flush=True)
'''
from langchain.chat_models import init_chat_model

model = init_chat_model(
    model='ollama:llama3.2:3b',
    base_url='http://localhost:11434/',
    temperature=0.3,
    timeout=30,
    max_token=1000
)
for chunk in model.stream('给我一篇现代诗词'):
    print(chunk.content, end='', flush=True)
'''
httpcore.ConnectError: 
[WinError 10061] 由于目标计算机积极拒绝，无法连接。
解决方法：启动Ollama.exe
'''
