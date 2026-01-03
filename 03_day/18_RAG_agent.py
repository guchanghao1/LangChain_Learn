# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
from langchain.agents import create_agent
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain.tools import tool

embedding = OllamaEmbeddings(
    model="qwen3-embedding:8b",
)

vector_store = Chroma(
    collection_name='rag_collection',
    embedding_function=embedding,
    persist_directory='./17_chroma_rag_bd',
)


@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """检索数据库的工具，来帮助回答用户的问题"""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    content = "\n\n".join(
        f"source:{doc.metadata}\ncontent{doc.page_content}" for doc in retrieved_docs
    )
    return content, retrieved_docs


load_dotenv()
system_prompt = """你是一个天体爱好者，通过检索工具的辅助回答用户问题。"""
agent = create_agent(
    model="deepseek:deepseek-chat",
    tools=[retrieve_context],
    system_prompt=system_prompt,
)

results = agent.invoke(
    {"messages": [{"role": "human", "content": "讲一下3i/Atlas."}]}
)

messages = results["messages"]
print(f"历史消息：{len(messages)}条")
for message in messages:
    message.pretty_print()
