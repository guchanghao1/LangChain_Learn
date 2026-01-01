# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

# 嵌入模型
embedding = OllamaEmbeddings(
    model='nomic-embed-text:latest'
)
# 向量库(知识库)
vector_store = Chroma(
    collection_name='example_collection',
    embedding_function=embedding,
    persist_directory='./chroma_langchain_bd',

)

# 查询：三种方式
# 1.相似度查询
print('相似度查询')

results = vector_store.similarity_search(
    '安全宣传标语？'  # 大模型用量化的数据表达语义
)

for i, result in enumerate(results, 1):
    print(f'{i}-{result.page_content[:50]}')

# 2.带分数的相似度查询
print('带分数的相似度查询')

results = vector_store.similarity_search_with_score(
    '安全宣传标语？'  # 大模型用量化的数据表达语义
)

for (doc, score) in results:  # unpacking(解包)
    print(score)
    print(doc.page_content[:100])
    # score数越小，相似度越高

# 3.用向量进行相似度查询(把输入转化为向量，再到向量数据库查询。与第一种等价，相当于拆分)
print('用向量进行相似度查询')

vector = embedding.embed_query(
    '安全宣传标语？'
)

results = vector_store.similarity_search_by_vector(vector)
for i, result in enumerate(results, 1):
    print(f'{i}-{result.page_content[:50]}')

# chain:langchain: 大模型、提示词模板、tools、output 等串成链。Runnable
print('用检索器查询，把相似度查询封装成检索器')
from typing import List
from langchain_core.documents import Document
from langchain_core.runnables import chain


@chain
def retriever(query: str) -> List[Document]:
    return vector_store.similarity_search(query, k=1)  # k是返回的数量，默认4.


results = retriever.invoke('安全宣传标语？')
for i, result in enumerate(results, 1):
    print(f'{i}-{result.page_content[:50]}')
