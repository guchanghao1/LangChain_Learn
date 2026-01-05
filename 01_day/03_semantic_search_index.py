# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
# 索引
# 1.读取pdf  按照页管理  Document  list[Document]
# 2.分割文本  文本段（chunk）  Document  list[Document]
# 3.向量化： 文本段<=>向量   需要嵌入模型辅助
# 4.向量库：把多个文本段/向量存入向量库
# pip install pypdf

# 1.读取pdf  按照页管理  Document  list[Document]
from langchain_community.document_loaders import PyPDFLoader

file_path = '03_text.pdf'

loader = PyPDFLoader(file_path)

docs = loader.load()

# print(len(docs))  # 48
# print(type(docs[0]))  # <class 'langchain_core.documents.base.Document'>
# print(docs[0])
'''
page_content='' 
metadata={
'producer': '', 
'creator': 'WPS 文字', 
'creationdate': '2024-11-13T14:41:54+06:41', 
'author': 'admin', 
'comments': '', 
'company': '', 
'keywords': '',
 'moddate': '2024-11-14T17:37:08+08:00', 
 'sourcemodified': "D:20241113144154+06'41'", 
 'subject': '', 
 'title': '', 
 'trapped': '/False', 
 'source': '03_text.pdf', 
 'total_pages': 48,
  'page': 0, 
  'page_label': '1'}
'''

# 2.分割文本  文本段（chunk）  Document  list[Document]
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # characters
    chunk_overlap=100,  # 中间存在重叠区域，使语义关联度加强
    add_start_index=True
)

all_splits = text_splitter.split_documents(docs)  # list[Document]
# print(len(all_splits))  # 52  与chunk_size=1000,有关
# print(all_splits[1])
'''
page_content='' 
 metadata={
'producer': '', 
'creator': 'WPS 文字', 
'creationdate': '2024-11-13T14:41:54+06:41',
'author': 'admin', 
'comments': '',
'company': '', 
'keywords': '', 
'moddate': '2024-11-14T17:37:08+08:00',
'sourcemodified': "D:20241113144154+06'41'",
'subject': '', 
'title': '',
'trapped': '/False', 
'source': '03_text.pdf', 
'total_pages': 48,
 'page': 1, 
'page_label': '2', 
'start_index': 0}

'''

# 3.向量化： 文本段<=>向量   需要嵌入模型辅助
from langchain_ollama import OllamaEmbeddings

embedding = OllamaEmbeddings(
    model="nomic-embed-text:latest",
)

'''
vector_0 = embedding.embed_query(all_splits[0].page_content)
print(len(vector_0))  # 768  向量长度。与嵌入模型的定义有关
print(vector_0)  # [0.0077065364, 0.017068036, -0.1393289,......,]
'''

# 4（3）.向量库：把多个文本段/向量存入向量库(融合第三步)
from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name='example_collection',
    embedding_function=embedding,
    persist_directory='./chroma_langchain_bd',
)

ids = vector_store.add_documents(documents=all_splits)
print(len(ids))
print(ids)
# 运行会记录存储内容，不可过多运行，会累计
# 删除目录，重建向量库
