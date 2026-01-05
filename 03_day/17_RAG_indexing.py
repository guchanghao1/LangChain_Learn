# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
# 索引
# 1.读取网页  按照页管理  Document  list[Document]
# 2.分割文本  文本段（chunk）  Document  list[Document]
# 3.向量化： 文本段<=>向量   需要嵌入模型辅助
# 4.向量库：把多个文本段/向量存入向量库
# pip install bs4
from langchain_community.document_loaders import WebBaseLoader
import bs4

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_ollama import OllamaEmbeddings

from langchain_chroma import Chroma

import os
import shutil

if os.path.exists("./17_chroma_rag_bd"):
    shutil.rmtree("./17_chroma_rag_bd")

# 1.读取网页  按照页管理  Document  list[Document]
page_urls = [
    "https://news.sciencenet.cn/htmlnews/2025/7/547139.shtm",
    "http://mrdx.cn/content/20250709/Articel05005NU.htm",
    "https://starwalk.space/zh-Hant/news/3i-atlas-interstellar-object",
    "https://news.sjtu.edu.cn/jdzh/20251205/217724.html"
]
for page_url in page_urls:
    bs4_strainer = bs4.SoupStrainer()

    loader = WebBaseLoader(
        web_path=page_url,
        bs_kwargs={"parse_only": bs4_strainer},
    )

    docs = loader.load()

    # 2.分割文本  文本段（chunk）  Document  list[Document]
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,  # characters
        chunk_overlap=200,  # 中间存在重叠区域，使语义关联度加强
        add_start_index=True
    )

    all_splits = text_splitter.split_documents(docs)  # list[Document]

    # 3.向量化： 文本段<=>向量   需要嵌入模型辅助
    embedding = OllamaEmbeddings(
        model="qwen3-embedding:8b",
    )

    # 4（3）.向量库：把多个文本段/向量存入向量库(融合第三步)
    vector_store = Chroma(
        collection_name='rag_collection',
        embedding_function=embedding,
        persist_directory='./17_chroma_rag_bd',
    )

    ids = vector_store.add_documents(documents=all_splits)
    print(len(ids))
