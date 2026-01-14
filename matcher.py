import faiss
import numpy as np
import os

DIM = 384  # MiniLM embedding size

def create_index():
    return faiss.IndexFlatIP(DIM)

def add_to_index(index, embeddings):
    faiss.normalize_L2(embeddings)
    index.add(embeddings)

def search(index, query_embedding, top_k):
    faiss.normalize_L2(query_embedding)
    scores, ids = index.search(query_embedding, top_k)
    return scores[0], ids[0]
