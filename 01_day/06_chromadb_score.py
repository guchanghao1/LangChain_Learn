# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# 嵌入模型
embedding = OllamaEmbeddings(
    model='qwen3-embedding:8b'
)

# 评分方式
score_measures = [
    'default',
    'cosine',  # 用两个向量的夹角度量相似度
    'l2',  # 用两个向量的距离度量相似度
    'ip'  # 用两个向量的内积/点积度量相似度
]

# 创建向量库和4个collection
persist_dir = 'chroma_score_db'
vector_stores = []
for score_measure in score_measures:
    collection_metadata = {'hnsw:space': score_measure}
    if score_measure == 'default':
        collection_metadata = None

    collection_name = f'my_collection_{score_measure}'
    vector_stores.append(
        Chroma(
            collection_name=collection_name,
            embedding_function=embedding,
            persist_directory=persist_dir,
            collection_metadata=collection_metadata,
        ))


def indexing(docs):
    print('\n加入文档：')
    for vector_store in vector_stores:
        ids = vector_store.add_documents(docs)
        print(f'\n集合：{vector_store._collection.name}')
        print(ids)


def query_with_score(query):
    for i in range(len(score_measures)):
        results = vector_stores[i].similarity_search_with_score(query)
        print(f'\n搜索：{query}')
        for doc, score in results:
            print(doc.page_content, end='')
            print(f'{score_measures[i]}: {score}')


""""""
docs = [
    Document(page_content='手机很好用'),
    Document(page_content='陕西地区盛产小米'),
]

indexing(docs)
'''
加入文档：

集合：my_collection_default
['52ea8fcd-d394-40b1-8b92-7c3625da1adf', 'd6bb7942-2804-48cf-b257-5f8cad8f6817']

集合：my_collection_cosine
['819e24e8-e90b-4279-a545-aa7c6faf3aa5', '5a990a74-20d4-467c-817e-8d7d6773527f']

集合：my_collection_l2
['cdd07aee-9017-4c6c-a4a8-264d76b4bd42', 'd10ee58c-4f6b-4cf5-b082-b2c0a41d32b8']

集合：my_collection_ip
['ba3ee2e7-6695-4bae-87de-d17ef87965e5', 'd60b1cb8-565f-4577-941d-b36e652b75ec']
'''


query_with_score('刚和朋友通完电话')
