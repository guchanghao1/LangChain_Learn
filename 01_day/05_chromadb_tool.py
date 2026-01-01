# !/usr/bin/env python
# -*- coding: utf-8 -*-
""""""
# ----------------------------------------------------------------------------------------------------------------------
import chromadb


# 列出向量库的collections和记录
def list_collection(db_path):
    client = chromadb.PersistentClient(db_path)
    collections = client.list_collections()
    print(f'chromadb:{db_path}--{len(collections)}个collections')

    for i, collection in enumerate(collections):
        print(f'collection {i}:{collection.name},共有{collection.count()}条记录')


def delete_collection(db_path, collection_name):
    try:
        client = chromadb.PersistentClient(db_path)
        client.delete_collection(collection_name)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    db_path = './chroma_langchain_bd'
    list_collection(db_path)
    # chromadb:./chroma_langchain_bd--1个collections
    # collection 0:example_collection,共有52条记录
